# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: raft.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'raft.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\"[\n\x0bVoteRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61ndidateId\x18\x02 \x01(\t\x12\x14\n\x0clastLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0blastLogTerm\x18\x04 \x01(\x05\"1\n\x0cVoteResponse\x12\x13\n\x0bvoteGranted\x18\x01 \x01(\x08\x12\x0c\n\x04term\x18\x02 \x01(\x05\"\x93\x01\n\x14\x41ppendEntriesRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08leaderId\x18\x02 \x01(\t\x12\x14\n\x0cprevLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0bprevLogTerm\x18\x04 \x01(\x05\x12\x1a\n\x07\x65ntries\x18\x05 \x03(\x0b\x32\t.LogEntry\x12\x14\n\x0cleaderCommit\x18\x06 \x01(\x05\"6\n\x15\x41ppendEntriesResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\")\n\x08LogEntry\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t2y\n\x0bRaftService\x12*\n\x0bRequestVote\x12\x0c.VoteRequest\x1a\r.VoteResponse\x12>\n\rAppendEntries\x12\x15.AppendEntriesRequest\x1a\x16.AppendEntriesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_VOTEREQUEST']._serialized_start=14
  _globals['_VOTEREQUEST']._serialized_end=105
  _globals['_VOTERESPONSE']._serialized_start=107
  _globals['_VOTERESPONSE']._serialized_end=156
  _globals['_APPENDENTRIESREQUEST']._serialized_start=159
  _globals['_APPENDENTRIESREQUEST']._serialized_end=306
  _globals['_APPENDENTRIESRESPONSE']._serialized_start=308
  _globals['_APPENDENTRIESRESPONSE']._serialized_end=362
  _globals['_LOGENTRY']._serialized_start=364
  _globals['_LOGENTRY']._serialized_end=405
  _globals['_RAFTSERVICE']._serialized_start=407
  _globals['_RAFTSERVICE']._serialized_end=528
# @@protoc_insertion_point(module_scope)