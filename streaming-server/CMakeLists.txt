if (SCENARIO STREQUAL "cdn")
    set(service "tc_streaming_service")
    include("${CMAKE_SOURCE_DIR}/script/service.cmake")
endif()
