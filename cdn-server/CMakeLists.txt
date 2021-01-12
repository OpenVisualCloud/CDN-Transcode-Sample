if (SCENARIO STREQUAL "cdn")
    set(service "tc_cdn_service")
    include("${CMAKE_SOURCE_DIR}/script/service.cmake")
endif()
