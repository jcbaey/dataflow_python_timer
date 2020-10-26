import logging
import sys
import json
import click
import time
from datetime import datetime
import apache_beam as beam
from apache_beam.options.pipeline_options import StandardOptions, SetupOptions, PipelineOptions
from apache_beam.io import ReadFromPubSub, WriteToPubSub, ReadFromText
from apache_beam.io.gcp import bigquery_tools
from apache_beam.io.gcp.bigquery import BigQueryWriteFn
from apache_beam.transforms import window
from apache_beam.transforms.window import TimestampedValue
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.transforms.userstate import TimerSpec
from apache_beam.transforms.userstate import on_timer

class TimerExample(beam.DoFn):
    EXPIRY_TIMER = TimerSpec('expiry', beam.TimeDomain.REAL_TIME)
    EXPIRY_TIMER_DURATION_SECONDS = 5

    def process(self, elem, timestamp=beam.DoFn.TimestampParam, expiry_timer=beam.DoFn.TimerParam(EXPIRY_TIMER)):
        (key, msg) = elem
        expiration = time.time() + TimerExample.EXPIRY_TIMER_DURATION_SECONDS
        logging.info('Current element (%s, %s, %s) => Setting the timer to %s', timestamp.to_utc_datetime(), key, msg, datetime.fromtimestamp(expiration))
        expiry_timer.set(expiration)
        yield elem

    @on_timer(EXPIRY_TIMER) 
    def expiry(self):
        logging.info("Timer expired after {} seconds".format(TimerExample.EXPIRY_TIMER_DURATION_SECONDS))

class UserOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument(
            '--subscription',
            type=str,
            required=True,
            help='The pubsub subscription to listen')

@click.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
@click.argument('pipeline_args', nargs=-1, type=click.UNPROCESSED)
def run(pipeline_args):
    logging.basicConfig(format="%(asctime)s - %(message)s", stream=sys.stdout, level=logging.INFO, datefmt="%Y-%m-%d %H:%M.%S")
    logging.getLogger().setLevel(logging.INFO)

    options = PipelineOptions(pipeline_args)
    user_options = options.view_as(UserOptions)
    standard_options = options.view_as(StandardOptions)
    setup_options = options.view_as(SetupOptions)

    standard_options.streaming = True
    setup_options.save_main_session = True 
    
    logging.info("Start pipeline")
   
    with beam.Pipeline(options=options) as p:
        (p | 'read pub/sub topic' >> ReadFromPubSub(subscription=user_options.subscription.get(), with_attributes=False)
                    | 'Parse JSON' >> beam.Map(json.loads)
                    | 'Add timestamps' >> beam.Map(lambda x: TimestampedValue(x, x["timestamp"]))
                    | 'Keyed on key attribute' >> beam.Map(lambda  x: (x["key"], x["data"]))
                    | 'Setup the timer' >> beam.ParDo(TimerExample())
        )
        
if __name__ == '__main__':
    run()

