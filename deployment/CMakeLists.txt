include("${CMAKE_SOURCE_DIR}/script/scan-all.cmake")

if(NOT REGISTRY)
    add_custom_target(update ${CMAKE_HOME_DIRECTORY}/script/update-image.sh)
endif()
