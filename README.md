# dataflow_python_timer

## Create a new pub/sub topic

```
$ export GOOGLE_CLOUD_PROJECT=**GOOGLE_CLOUD_PROJECT**
$ export TOPIC_NAME=test_timer_topic
$ export SUB_NAME=test_timer_sub
$ export SERVICE_ACCOUNT=**SERVICE_ACCOUNT**
```

```
$ gcloud pubsub topics create $TOPIC_NAME
```

## Create the corresponding subscription

```
$ gcloud pubsub subscriptions create $SUB_NAME --topic $TOPIC_NAME  --expiration-period=24h
```

## Install python dependencies

```
$ pipenv install
```

## Start the pipeline locally with direct runner

```
$ python main.py \
  --subscription projects/$GOOGLE_CLOUD_PROJECT/subscriptions/$SUB_NAME \
  --service_account_email $SERVICE_ACCOUNT
  ```

### Send message to the pub/sub topic to start the timer

```
$ gcloud pubsub topics publish $TOPIC_NAME --message="{\"timestamp\": `date +%s`, \"key\": \"A\", \"data\": \"Element1\"}"
```

### Result

- It is working properly:

```
2020-10-26 14:09.58 - Start pipeline
2020-10-26 14:09.58 - Missing pipeline option (runner). Executing pipeline using the default runner: DirectRunner.
2020-10-26 14:09.58 - Key coder FastPrimitivesCoder for transform <ParDo(PTransform) label=[Setup the timer]> with stateful DoFn may not be deterministic. This may cause incorrect behavior for complex key types. Consider adding an input type hint for this transform.
2020-10-26 14:09.59 - Running pipeline with DirectRunner.
2020-10-26 14:10.05 - Current element (2020-10-26 13:10:04, A, Element1) => Set the timer to 2020-10-26 14:10:10.926540
2020-10-26 14:10.14 - Timer expired after 5 seconds
```

## Start the pipeline with dataflow runner

### With runner v1

```
python main.py \
  --subscription projects/$GOOGLE_CLOUD_PROJECT/subscriptions/$SUB_NAME \
  --runner DataflowRunner \
  --project $GOOGLE_CLOUD_PROJECT \
  --region europe-west1 \
  --no_use_public_ips \
  --network=***vpc-network*** \
  --subnetwork=***subnet1*** \
  --temp_location gs://**temp location**/ \
  --service_account_email $SERVICE_ACCOUNT
```

#### Send message to the pub/sub topic to start the timer

```
$ gcloud pubsub topics publish $TOPIC_NAME --message="{\"timestamp\": `date +%s`, \"key\": \"A\", \"data\": \"Element1\"}"
```

#### Result

- The error is the same as described in the [JIRA](https://issues.apache.org/jira/browse/BEAM-10786):

```
2020-10-26 14:15.36 - Created job with id: [2020-10-26_06_15_34-14192478891358881254]
2020-10-26 14:15.36 - Submitted job: 2020-10-26_06_15_34-14192478891358881254
2020-10-26 14:15.36 - Job 2020-10-26_06_15_34-14192478891358881254 is in state JOB_STATE_PENDING
2020-10-26 14:15.42 - 2020-10-26T13:15:39.787Z: JOB_MESSAGE_BASIC: Worker configuration: n1-standard-4 in europe-west1-d.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.545Z: JOB_MESSAGE_DETAILED: Expanding SplittableParDo operations into optimizable parts.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.550Z: JOB_MESSAGE_DETAILED: Expanding CollectionToSingleton operations into optimizable parts.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.566Z: JOB_MESSAGE_DETAILED: Expanding CoGroupByKey operations into optimizable parts.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.578Z: JOB_MESSAGE_DETAILED: Expanding SplittableProcessKeyed operations into optimizable parts.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.581Z: JOB_MESSAGE_DETAILED: Expanding GroupByKey operations into streaming Read/Write steps
2020-10-26 14:15.42 - 2020-10-26T13:15:40.586Z: JOB_MESSAGE_DEBUG: Annotating graph with Autotuner information.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.604Z: JOB_MESSAGE_DETAILED: Fusing adjacent ParDo, Read, Write, and Flatten operations
2020-10-26 14:15.42 - 2020-10-26T13:15:40.607Z: JOB_MESSAGE_DETAILED: Fusing consumer Parse JSON into read pub/sub topic/Read
2020-10-26 14:15.42 - 2020-10-26T13:15:40.610Z: JOB_MESSAGE_DETAILED: Fusing consumer Add timestamps into Parse JSON
2020-10-26 14:15.42 - 2020-10-26T13:15:40.613Z: JOB_MESSAGE_DETAILED: Fusing consumer Keyed on key attribute into Add timestamps
2020-10-26 14:15.42 - 2020-10-26T13:15:40.634Z: JOB_MESSAGE_DEBUG: Adding StepResource setup and teardown to workflow graph.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.654Z: JOB_MESSAGE_DEBUG: Adding workflow start and stop steps.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.707Z: JOB_MESSAGE_DEBUG: Assigning stage ids.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.911Z: JOB_MESSAGE_DEBUG: Executing wait step start2
2020-10-26 14:15.42 - 2020-10-26T13:15:40.931Z: JOB_MESSAGE_DEBUG: Starting worker pool setup.
2020-10-26 14:15.42 - 2020-10-26T13:15:40.939Z: JOB_MESSAGE_BASIC: Starting 1 workers...
2020-10-26 14:15.42 - Job 2020-10-26_06_15_34-14192478891358881254 is in state JOB_STATE_RUNNING
2020-10-26 14:15.47 - 2020-10-26T13:15:43.232Z: JOB_MESSAGE_BASIC: Executing operation read pub/sub topic/Read+Parse JSON+Add timestamps+Keyed on key attribute+Keyed on key attribute.out/FromValue/WriteStream
2020-10-26 14:15.47 - 2020-10-26T13:15:43.237Z: JOB_MESSAGE_BASIC: Executing operation Keyed on key attribute.out/FromValue/ReadStream+Setup the timer
2020-10-26 14:16.08 - 2020-10-26T13:16:06.312Z: JOB_MESSAGE_DEBUG: Executing input step topology_init_attach_disk_input_step
2020-10-26 14:16.08 - 2020-10-26T13:16:07.104Z: JOB_MESSAGE_BASIC: Worker configuration: n1-standard-4 in europe-west1-d.
2020-10-26 14:16.49 - 2020-10-26T13:16:44.223Z: JOB_MESSAGE_DETAILED: Workers have started successfully.
2020-10-26 14:17.56 - 2020-10-26T13:17:52.640Z: JOB_MESSAGE_ERROR: java.util.concurrent.ExecutionException: java.lang.RuntimeException: Error received from SDK harness for instruction -46: Traceback (most recent call last):
  File "/usr/local/lib/python3.8/site-packages/apache_beam/runners/worker/sdk_worker.py", line 258, in _execute
    response = task()
  File "/usr/local/lib/python3.8/site-packages/apache_beam/runners/worker/sdk_worker.py", line 315, in <lambda>
    lambda: self.create_worker().do_instruction(request), request)
  File "/usr/local/lib/python3.8/site-packages/apache_beam/runners/worker/sdk_worker.py", line 483, in do_instruction
    return getattr(self, request_type)(
  File "/usr/local/lib/python3.8/site-packages/apache_beam/runners/worker/sdk_worker.py", line 519, in process_bundle
    bundle_processor.process_bundle(instruction_id))
  File "/usr/local/lib/python3.8/site-packages/apache_beam/runners/worker/bundle_processor.py", line 966, in process_bundle
    output_stream = self.timer_data_channel.output_timer_stream(
AttributeError: 'NoneType' object has no attribute 'output_timer_stream'
```

### With runner v2 and streaming engine

```
python main.py \
  --subscription projects/$GOOGLE_CLOUD_PROJECT/subscriptions/$SUB_NAME \
  --runner DataflowRunner \
  --project $GOOGLE_CLOUD_PROJECT \
  --region europe-west1 \
  --no_use_public_ips \
  --network=**vpc network** \
  --subnetwork=regions/europe-west1/subnetworks/***subnet*** \
  --temp_location gs://***temp location***/ \
  --service_account_email $SERVICE_ACCOUNT \
  --enable_streaming_engine \
  --max_num_workers=1 \
  --experiments=use_runner_v2
  ```


#### Send message to the pub/sub topic to start the timer

```
gcloud pubsub topics publish $TOPIC_NAME --message="{\"timestamp\": `date +%s`, \"key\": \"A\", \"data\": \"Element1\"}"
```
 
 #### Result

- The pipeline starts correctly:

 ```
 2020-10-26 14:19.12 - 2020-10-26T13:19:05.678Z: JOB_MESSAGE_DETAILED: Autoscaling was automatically enabled for job 2020-10-26_06_19_05-11247069410789502909.
2020-10-26 14:19.12 - 2020-10-26T13:19:05.678Z: JOB_MESSAGE_WARNING: Autoscaling is enabled for Dataflow Streaming Engine. Workers will scale between 1 and 100 unless maxNumWorkers is specified.
2020-10-26 14:19.12 - 2020-10-26T13:19:05.678Z: JOB_MESSAGE_DETAILED: Autoscaling is enabled for job 2020-10-26_06_19_05-11247069410789502909. The number of workers will be between 1 and 100.
2020-10-26 14:19.12 - 2020-10-26T13:19:10.430Z: JOB_MESSAGE_BASIC: Worker configuration: n1-standard-2 in europe-west1-d.
2020-10-26 14:19.12 - 2020-10-26T13:19:11.233Z: JOB_MESSAGE_DETAILED: Expanding SplittableParDo operations into optimizable parts.
2020-10-26 14:19.12 - 2020-10-26T13:19:11.267Z: JOB_MESSAGE_DETAILED: Expanding CollectionToSingleton operations into optimizable parts.
2020-10-26 14:19.12 - 2020-10-26T13:19:11.332Z: JOB_MESSAGE_DETAILED: Expanding CoGroupByKey operations into optimizable parts.
2020-10-26 14:19.12 - 2020-10-26T13:19:11.372Z: JOB_MESSAGE_DETAILED: Expanding SplittableProcessKeyed operations into optimizable parts.
2020-10-26 14:19.12 - 2020-10-26T13:19:11.403Z: JOB_MESSAGE_DETAILED: Expanding GroupByKey operations into streaming Read/Write steps
2020-10-26 14:19.12 - 2020-10-26T13:19:11.433Z: JOB_MESSAGE_DETAILED: Lifting ValueCombiningMappingFns into MergeBucketsMappingFns
2020-10-26 14:19.12 - 2020-10-26T13:19:11.470Z: JOB_MESSAGE_DEBUG: Annotating graph with Autotuner information.
2020-10-26 14:19.12 - 2020-10-26T13:19:11.508Z: JOB_MESSAGE_DETAILED: Fusing adjacent ParDo, Read, Write, and Flatten operations
2020-10-26 14:19.12 - 2020-10-26T13:19:11.537Z: JOB_MESSAGE_DETAILED: Fusing consumer Parse JSON into read pub/sub topic/Read
2020-10-26 14:19.12 - 2020-10-26T13:19:11.570Z: JOB_MESSAGE_DETAILED: Fusing consumer Add timestamps into Parse JSON
2020-10-26 14:19.12 - 2020-10-26T13:19:11.603Z: JOB_MESSAGE_DETAILED: Fusing consumer Keyed on key attribute into Add timestamps
2020-10-26 14:19.12 - 2020-10-26T13:19:11.707Z: JOB_MESSAGE_DEBUG: Workflow config is missing a default resource spec.
2020-10-26 14:19.12 - 2020-10-26T13:19:11.738Z: JOB_MESSAGE_DEBUG: Adding StepResource setup and teardown to workflow graph.
2020-10-26 14:19.12 - 2020-10-26T13:19:11.771Z: JOB_MESSAGE_DEBUG: Adding workflow start and stop steps.
2020-10-26 14:19.12 - 2020-10-26T13:19:11.804Z: JOB_MESSAGE_DEBUG: Assigning stage ids.
2020-10-26 14:19.12 - Job 2020-10-26_06_19_05-11247069410789502909 is in state JOB_STATE_RUNNING
2020-10-26 14:19.17 - 2020-10-26T13:19:13.012Z: JOB_MESSAGE_DEBUG: Starting worker pool setup.
2020-10-26 14:19.17 - 2020-10-26T13:19:13.061Z: JOB_MESSAGE_DEBUG: Starting worker pool setup.
2020-10-26 14:19.17 - 2020-10-26T13:19:13.093Z: JOB_MESSAGE_BASIC: Starting 1 workers in europe-west1-d...
2020-10-26 14:19.38 - 2020-10-26T13:19:36.773Z: JOB_MESSAGE_DETAILED: Autoscaling: Raised the number of workers to 1 so that the pipeline can catch up with its backlog and keep up with its input rate.
2020-10-26 14:20.34 - 2020-10-26T13:20:31.241Z: JOB_MESSAGE_DETAILED: Workers have started successfully.
2020-10-26 14:20.34 - 2020-10-26T13:20:31.267Z: JOB_MESSAGE_DETAILED: Workers have started successfully.
```

- However the worker has no timer expiry logs and it looks like it restarts periodically.

```
2020-10-26 14:35:48.562 CETLogging handler created.
2020-10-26 14:35:48.566 CETsemi_persistent_directory: /var/opt/google
2020-10-26 14:35:48.576 CETStatus HTTP server running at localhost:34343
2020-10-26 14:35:48.588 CETDiscarding unparseable args: ['--autoscalingAlgorithm=NONE', '--beam_plugins=apache_beam.io.filesystem.FileSystem', '--beam_plugins=apache_beam.io.hadoopfilesystem.HadoopFileSystem', '--beam_plugins=apache_beam.io.localfilesystem.LocalFileSystem', '--beam_plugins=apache_beam.io.gcp.gcsfilesystem.GCSFileSystem', '--beam_plugins=apache_beam.io.aws.s3filesystem.S3FileSystem', '--beam_plugins=apache_beam.io.azure.blobstoragefilesystem.BlobStorageFileSystem', '--dataflowJobId=2020-10-26_06_33_25-11189494018058803226', '--direct_runner_use_stacked_bundle', '--gcpTempLocation=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', '--job_server_timeout=60', '--maxNumWorkers=1', '--numWorkers=1', '--pipelineUrl=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864/pipeline.pb', '--pipeline_type_check']
2020-10-26 14:35:48.590 CETPython sdk harness started with pipeline_options: {'runner': 'DataflowRunner', 'streaming': True, 'project': '**GOOGLE_CLOUD_PROJECT**', 'job_name': 'beamapp-az02050-1026133321-495637', 'staging_location': 'gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', 'temp_location': 'gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', 'region': 'europe-west1', 'service_account_email': '**SERVICE_ACCOUNT**', 'enable_streaming_engine': True, 'max_num_workers': 1, 'network': '**vpc network**', 'subnetwork': 'regions/europe-west1/subnetworks/***subnet***', 'experiments': ['use_runner_v2', 'use_unified_worker', 'beam_fn_api', 'enable_windmill_service', 'enable_streaming_engine', 'use_fastavro', 'use_multiple_sdk_containers'], 'save_main_session': True, 'sdk_worker_parallelism': '1', 'environment_cache_millis': '0', 'job_port': '0', 'artifact_port': '0', 'expansion_port': '0', 'subscription': <apache_beam.options.value_provider.StaticValueProvider object at 0x7fdebb341460>}
2020-10-26 14:35:48.595 CETCreating state cache with size 0
2020-10-26 14:35:48.596 CETCreating insecure control channel for localhost:12371.
2020-10-26 14:35:48.598 CETControl channel established.
2020-10-26 14:35:48.604 CETInitializing SDKHarness with unbounded number of workers.
2020-10-26 14:35:48.618 CETLogging handler created.
2020-10-26 14:35:48.620 CETsemi_persistent_directory: /var/opt/google
2020-10-26 14:35:48.626 CETStatus HTTP server running at localhost:43833
2020-10-26 14:35:48.634 CETDiscarding unparseable args: ['--autoscalingAlgorithm=NONE', '--beam_plugins=apache_beam.io.filesystem.FileSystem', '--beam_plugins=apache_beam.io.hadoopfilesystem.HadoopFileSystem', '--beam_plugins=apache_beam.io.localfilesystem.LocalFileSystem', '--beam_plugins=apache_beam.io.gcp.gcsfilesystem.GCSFileSystem', '--beam_plugins=apache_beam.io.aws.s3filesystem.S3FileSystem', '--beam_plugins=apache_beam.io.azure.blobstoragefilesystem.BlobStorageFileSystem', '--dataflowJobId=2020-10-26_06_33_25-11189494018058803226', '--direct_runner_use_stacked_bundle', '--gcpTempLocation=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', '--job_server_timeout=60', '--maxNumWorkers=1', '--numWorkers=1', '--pipelineUrl=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864/pipeline.pb', '--pipeline_type_check']
2020-10-26 14:36:06.295 CET{"job":"2020-10-26_06_33_25-11189494018058803226","logger":"/usr/local/lib/python3.8/site-packages/apache_beam/runners/worker/sdk_worker_main.py:136","message":"Python sdk harness started with pipeline_options: {'runner': 'DataflowRunner', 'streaming': True, 'project': '**GOOGLE_CLOUD_PROJECT**', 'job_name': 'beamapp-az02050-1026133321-495637', 'staging_location': 'gs://rs
2020-10-26 14:36:19.429 CETCreating insecure state channel for localhost:12371.
2020-10-26 14:36:19.429 CETState channel established.
2020-10-26 14:36:19.431 CETCreating insecure state channel for localhost:12371.
2020-10-26 14:36:19.431 CETState channel established.
2020-10-26 14:36:19.433 CETCreating client data channel for localhost:12371
2020-10-26 14:36:19.439 CETCreating client data channel for localhost:12371
2020-10-26 14:36:19.990 CETCurrent element (2020-10-26 13:27:07, A, Element1) => Setting the timer to 2020-10-26 13:36:24.990280
2020-10-26 14:36:19.992 CETCurrent element (2020-10-26 13:34:33, A, Element1) => Setting the timer to 2020-10-26 13:36:24.992256
2020-10-26 14:36:26.295 CETl-***-d-gsb-euwe1-tmp/beamapp-az02050-1026133321-495637.1603719201.495864', 'temp_location': 'gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', 'region': 'europe-west1', 'service_account_email': '**SERVICE_ACCOUNT**', 'enable_streaming_engine': True, 'max_num_workers': 1, 'network': '**vpc network**', 'subnetwork': 'regions/europe-west1/subnetworks/***subnet***', 'experiments': ['use_runner_v2', 'use_unified_worker', 'beam_fn_api', 'enable_windmill_service', 'enable_streaming_engine', 'use_fastavro', 'use_multiple_sdk_containers'], 'save_main_session': True, 'sdk_worker_parallelism': '1', 'environment_cache_millis': '0', 'job_port': '0', 'artifact_port': '0', 'expansion_port': '0', 'subscription': <apache_beam.options.value_provider.StaticValueProvider object at 0x7fa38a661520>}","portability_worker_id":"sdk-0-1","severity":"INFO","thread":"MainThread","timestamp":{"nanos":635949373,"seconds":1603719348},"worker":"beamapp-az02050-102613332-10260633-dijv-harness-gbjq"}
2020-10-26 14:36:47.714 CETLogging handler created.
2020-10-26 14:36:47.721 CETsemi_persistent_directory: /var/opt/google
2020-10-26 14:36:47.729 CETStatus HTTP server running at localhost:43335
2020-10-26 14:36:47.776 CETDiscarding unparseable args: ['--autoscalingAlgorithm=NONE', '--beam_plugins=apache_beam.io.filesystem.FileSystem', '--beam_plugins=apache_beam.io.hadoopfilesystem.HadoopFileSystem', '--beam_plugins=apache_beam.io.localfilesystem.LocalFileSystem', '--beam_plugins=apache_beam.io.gcp.gcsfilesystem.GCSFileSystem', '--beam_plugins=apache_beam.io.aws.s3filesystem.S3FileSystem', '--beam_plugins=apache_beam.io.azure.blobstoragefilesystem.BlobStorageFileSystem', '--dataflowJobId=2020-10-26_06_33_25-11189494018058803226', '--direct_runner_use_stacked_bundle', '--gcpTempLocation=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', '--job_server_timeout=60', '--maxNumWorkers=1', '--numWorkers=1', '--pipelineUrl=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864/pipeline.pb', '--pipeline_type_check']
2020-10-26 14:36:47.781 CETPython sdk harness started with pipeline_options: {'runner': 'DataflowRunner', 'streaming': True, 'project': '**GOOGLE_CLOUD_PROJECT**', 'job_name': 'beamapp-az02050-1026133321-495637', 'staging_location': 'gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', 'temp_location': 'gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', 'region': 'europe-west1', 'service_account_email': '**SERVICE_ACCOUNT**', 'enable_streaming_engine': True, 'max_num_workers': 1, 'network': '**vpc network**', 'subnetwork': 'regions/europe-west1/subnetworks/***subnet***', 'experiments': ['use_runner_v2', 'use_unified_worker', 'beam_fn_api', 'enable_windmill_service', 'enable_streaming_engine', 'use_fastavro', 'use_multiple_sdk_containers'], 'save_main_session': True, 'sdk_worker_parallelism': '1', 'environment_cache_millis': '0', 'job_port': '0', 'artifact_port': '0', 'expansion_port': '0', 'subscription': <apache_beam.options.value_provider.StaticValueProvider object at 0x7ff9997a15b0>}
2020-10-26 14:36:47.796 CETCreating state cache with size 0
2020-10-26 14:36:47.796 CETCreating insecure control channel for localhost:12371.
2020-10-26 14:36:47.821 CETControl channel established.
2020-10-26 14:36:47.890 CETInitializing SDKHarness with unbounded number of workers.
2020-10-26 14:36:48.635 CETLogging handler created.
2020-10-26 14:36:48.640 CETsemi_persistent_directory: /var/opt/google
2020-10-26 14:36:48.642 CETStatus HTTP server running at localhost:44701
2020-10-26 14:36:48.674 CETDiscarding unparseable args: ['--autoscalingAlgorithm=NONE', '--beam_plugins=apache_beam.io.filesystem.FileSystem', '--beam_plugins=apache_beam.io.hadoopfilesystem.HadoopFileSystem', '--beam_plugins=apache_beam.io.localfilesystem.LocalFileSystem', '--beam_plugins=apache_beam.io.gcp.gcsfilesystem.GCSFileSystem', '--beam_plugins=apache_beam.io.aws.s3filesystem.S3FileSystem', '--beam_plugins=apache_beam.io.azure.blobstoragefilesystem.BlobStorageFileSystem', '--dataflowJobId=2020-10-26_06_33_25-11189494018058803226', '--direct_runner_use_stacked_bundle', '--gcpTempLocation=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', '--job_server_timeout=60', '--maxNumWorkers=1', '--numWorkers=1', '--pipelineUrl=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864/pipeline.pb', '--pipeline_type_check']
2020-10-26 14:36:48.677 CETPython sdk harness started with pipeline_options: {'runner': 'DataflowRunner', 'streaming': True, 'project': '**GOOGLE_CLOUD_PROJECT**', 'job_name': 'beamapp-az02050-1026133321-495637', 'staging_location': 'gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', 'temp_location': 'gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', 'region': 'europe-west1', 'service_account_email': '**SERVICE_ACCOUNT**', 'enable_streaming_engine': True, 'max_num_workers': 1, 'network': '**vpc network**', 'subnetwork': 'regions/europe-west1/subnetworks/***subnet***', 'experiments': ['use_runner_v2', 'use_unified_worker', 'beam_fn_api', 'enable_windmill_service', 'enable_streaming_engine', 'use_fastavro', 'use_multiple_sdk_containers'], 'save_main_session': True, 'sdk_worker_parallelism': '1', 'environment_cache_millis': '0', 'job_port': '0', 'artifact_port': '0', 'expansion_port': '0', 'subscription': <apache_beam.options.value_provider.StaticValueProvider object at 0x7f5e9f1e04c0>}
2020-10-26 14:36:48.684 CETCreating state cache with size 0
2020-10-26 14:36:48.684 CETCreating insecure control channel for localhost:12371.
2020-10-26 14:36:48.687 CETControl channel established.
2020-10-26 14:36:48.695 CETInitializing SDKHarness with unbounded number of workers.
2020-10-26 14:36:56.556 CETCreating insecure state channel for localhost:12371.
2020-10-26 14:36:56.556 CETCreating insecure state channel for localhost:12371.
2020-10-26 14:36:56.556 CETState channel established.
2020-10-26 14:36:56.557 CETState channel established.
2020-10-26 14:36:56.559 CETCreating client data channel for localhost:12371
2020-10-26 14:36:56.560 CETCreating client data channel for localhost:12371
2020-10-26 14:36:56.589 CETCurrent element (2020-10-26 13:27:07, A, Element1) => Setting the timer to 2020-10-26 13:37:01.589393
2020-10-26 14:36:56.590 CETCurrent element (2020-10-26 13:34:33, A, Element1) => Setting the timer to 2020-10-26 13:37:01.589949
2020-10-26 14:36:56.590 CETCurrent element (2020-10-26 13:28:37, A, Element1) => Setting the timer to 2020-10-26 13:37:01.590296
2020-10-26 14:37:19.383 CETLogging handler created.
2020-10-26 14:37:19.388 CETsemi_persistent_directory: /var/opt/google
2020-10-26 14:37:19.396 CETStatus HTTP server running at localhost:36233
2020-10-26 14:37:19.412 CETDiscarding unparseable args: ['--autoscalingAlgorithm=NONE', '--beam_plugins=apache_beam.io.filesystem.FileSystem', '--beam_plugins=apache_beam.io.hadoopfilesystem.HadoopFileSystem', '--beam_plugins=apache_beam.io.localfilesystem.LocalFileSystem', '--beam_plugins=apache_beam.io.gcp.gcsfilesystem.GCSFileSystem', '--beam_plugins=apache_beam.io.aws.s3filesystem.S3FileSystem', '--beam_plugins=apache_beam.io.azure.blobstoragefilesystem.BlobStorageFileSystem', '--dataflowJobId=2020-10-26_06_33_25-11189494018058803226', '--direct_runner_use_stacked_bundle', '--gcpTempLocation=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', '--job_server_timeout=60', '--maxNumWorkers=1', '--numWorkers=1', '--pipelineUrl=gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864/pipeline.pb', '--pipeline_type_check']
2020-10-26 14:37:19.414 CETPython sdk harness started with pipeline_options: {'runner': 'DataflowRunner', 'streaming': True, 'project': '**GOOGLE_CLOUD_PROJECT**', 'job_name': 'beamapp-az02050-1026133321-495637', 'staging_location': 'gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', 'temp_location': 'gs://***temp location***/beamapp-az02050-1026133321-495637.1603719201.495864', 'region': 'europe-west1', 'service_account_email': '**SERVICE_ACCOUNT**', 'enable_streaming_engine': True, 'max_num_workers': 1, 'network': '**vpc network**', 'subnetwork': 'regions/europe-west1/subnetworks/***subnet***', 'experiments': ['use_runner_v2', 'use_unified_worker', 'beam_fn_api', 'enable_windmill_service', 'enable_streaming_engine', 'use_fastavro', 'use_multiple_sdk_containers'], 'save_main_session': True, 'sdk_worker_parallelism': '1', 'environment_cache_millis': '0', 'job_port': '0', 'artifact_port': '0', 'expansion_port': '0', 'subscription': <apache_beam.options.value_provider.StaticValueProvider object at 0x7f8cb22a2520>}
2020-10-26 14:37:19.420 CETCreating state cache with size 0
...

```

