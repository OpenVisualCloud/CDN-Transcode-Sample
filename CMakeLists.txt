cmake_minimum_required (VERSION 2.8)

Project(CDNTranscodeSample NONE)

if (NOT DEFINED REGISTRY)
    set(REGISTRY "")
elseif (NOT ${REGISTRY} MATCHES "/$")
    set(REGISTRY "${REGISTRY}/")
endif()
if (NOT DEFINED NVODS)
    set(NVODS "2")
endif()
if (NOT DEFINED NLIVES)
    set(NLIVES "1")
endif()

if (NOT DEFINED PLATFORM)
    set(PLATFORM "Xeon")
endif()

if (NOT DEFINED SCENARIO)
    set(SCENARIO "transcode")
endif()

if (NOT (SCENARIO STREQUAL "cdn"))
    set(NLIVES "0")
endif()

file(GLOB dirs "deployment" "*")
list(REMOVE_DUPLICATES dirs)
foreach(dir ${dirs})
    if(EXISTS ${dir}/CMakeLists.txt)
        add_subdirectory(${dir})
    endif()
endforeach()

# legal message
execute_process(COMMAND printf "\nThis script will build third party components licensed under various open source licenses into your container images. The terms under which those components may be used and distributed can be found with the license document that is provided with those components. Please familiarize yourself with those terms to ensure your distribution of those components complies with the terms of those licenses.\n\n")
execute_process(COMMAND printf "\n-- Setting: PLATFORM=${PLATFORM} SCENARIO=${SCENARIO}\n")
execute_process(COMMAND printf "-- Setting: NVODS=${NVODS}, NLIVES=${NLIVES}\n")
execute_process(COMMAND printf "-- Setting: REGISTRY=${REGISTRY}\n")
