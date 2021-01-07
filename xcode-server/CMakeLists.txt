set(service "ovc_transcode_service")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
add_dependencies(build_${service} build_ovc_cdn_common)
