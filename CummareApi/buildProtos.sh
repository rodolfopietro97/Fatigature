# Build protos
python -m grpc_tools.protoc -I./Protos --python_out=./Clients --grpc_python_out=./Clients ./Protos/*.proto

# NOTE: remember to add "Utils.CummareApi.Clients." in pb2_grpx.py imports