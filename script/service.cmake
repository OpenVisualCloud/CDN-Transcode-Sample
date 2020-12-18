if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/build.sh")
    add_custom_target(build_${service} ALL "${CMAKE_CURRENT_SOURCE_DIR}/build.sh" "${NVODS}" "${NLIVES}" "${SCENARIO}" "${PLATFORM}" "${REGISTRY}")
endif()
