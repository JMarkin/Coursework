cmake_minimum_required( VERSION 2.8 )

set(CMAKE_CXX_STANDARD 11)

project( BoostPythonHelloWorld )

find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()
# Find necessary packages
find_package( PythonLibs 2.7 REQUIRED )
include_directories( ${PYTHON_INCLUDE_DIRS} )
 
find_package( Boost COMPONENTS python REQUIRED )
include_directories( ${Boost_INCLUDE_DIR} )
 
# Build our library
add_library( greet SHARED Matrix.cpp )
 
# Define the wrapper library that wraps our library
add_library( Matrix SHARED greet_ext.cpp )
target_link_libraries( Matrix ${Boost_LIBRARIES} greet )
# don't prepend wrapper library name with lib
set_target_properties( Matrix PROPERTIES PREFIX "" )
