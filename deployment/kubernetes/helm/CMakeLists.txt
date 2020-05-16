set(service "helm")
include("${CMAKE_SOURCE_DIR}/script/service.cmake")
include("${CMAKE_SOURCE_DIR}/script/deployment.cmake")
add_custom_target(volume ${CMAKE_CURRENT_SOURCE_DIR}/mkvolume.sh)
