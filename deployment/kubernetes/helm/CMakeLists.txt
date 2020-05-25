set(service "helm")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")
add_dependencies(build_${service} build_pv)
