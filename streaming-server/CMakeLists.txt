set(service "ovc_streaming_service")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_ovc_transcode_sw)
