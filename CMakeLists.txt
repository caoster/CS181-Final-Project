cmake_minimum_required(VERSION 3.23)
set(CMAKE_CXX_STANDARD 17)

set(CHESS "Chinese_Chess")
project(${CHESS} VERSION 0.0.1)
add_subdirectory(JUCE)
file(GLOB INCLUDE_FILE include/*.h src/*.cpp main.cpp)
file(GLOB RANDOM RandomAgent/*.h RandomAgent/*.cpp)

macro(setup name)
    juce_add_gui_app(${name} PRODUCT_NAME ${name})
    juce_generate_juce_header(${name})
    target_compile_definitions(${name}
        PRIVATE
        # JUCE_WEB_BROWSER and JUCE_USE_CURL would be on by default, but you might not need them.
        JUCE_WEB_BROWSER=0
        JUCE_USE_CURL=0
        )
    target_link_libraries(${name}
            PRIVATE
            juce::juce_analytics
            juce::juce_audio_basics
            juce::juce_audio_devices
            juce::juce_audio_formats
            juce::juce_audio_plugin_client
            juce::juce_audio_processors
            juce::juce_audio_utils
            juce::juce_box2d
            juce::juce_core
            juce::juce_cryptography
            juce::juce_data_structures
            juce::juce_dsp
            juce::juce_events
            juce::juce_graphics
            juce::juce_gui_basics
            juce::juce_gui_extra
            juce::juce_opengl
            juce::juce_osc
            juce::juce_product_unlocking
            juce::juce_video
            PUBLIC
            juce::juce_recommended_config_flags
            juce::juce_recommended_warning_flags)
    target_sources(${name}
            PRIVATE
            ${INCLUDE_FILE}
            ${RANDOM}
            )
endmacro(setup)

setup(${CHESS})
#target_include_directories(${CHESS} PRIVATE Node1)

include_directories(${Boost_INCLUDE_DIR})