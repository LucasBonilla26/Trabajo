import os
import sys

import grpc
from chirpstack_api.as_pb.external import api

# Configuration.

# This must point to the API interface.
server = "158.49.112.190:8081"

# The DevEUI for which you want to enqueue the downlink.
dev_eui = bytes([0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01])

# The API token (retrieved using the web-interface).
api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5X2lkIjoiYmU5OTE3MDEtMmQzNC00YzQzLWJjNGItY2I1MjM1YTAxZmY2IiwiYXVkIjoiYXMiLCJpc3MiOiJhcyIsIm5iZiI6MTYzNjEzNTcyNywic3ViIjoiYXBpX2tleSJ9.1fZoIAL68Eu_1Iy27gsDC7c8uSG-2ehOZpxhm6OerMg"

if __name__ == "__main__":
  # Connect without using TLS.
  channel = grpc.insecure_channel(server)

  # Device-queue API client.
  client = api.DeviceQueueServiceStub(channel)

  # Define the API key meta-data.
  auth_token = [("authorization", "Bearer %s" % api_token)]

  # Construct request.
  req = api.EnqueueDeviceQueueItemRequest()
  req.device_queue_item.confirmed = False
  req.device_queue_item.data = bytes([0x0D, 0x01])
  req.device_queue_item.dev_eui = dev_eui.hex()
  req.device_queue_item.f_port = 10

  resp = client.Enqueue(req, metadata=auth_token)

  # Print the downlink frame-counter value.
  print(resp.f_cnt)

