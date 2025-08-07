find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_UDSIO gnuradio-udsio)

FIND_PATH(
    GR_UDSIO_INCLUDE_DIRS
    NAMES gnuradio/udsio/api.h
    HINTS $ENV{UDSIO_DIR}/include
        ${PC_UDSIO_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_UDSIO_LIBRARIES
    NAMES gnuradio-udsio
    HINTS $ENV{UDSIO_DIR}/lib
        ${PC_UDSIO_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-udsioTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_UDSIO DEFAULT_MSG GR_UDSIO_LIBRARIES GR_UDSIO_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_UDSIO_LIBRARIES GR_UDSIO_INCLUDE_DIRS)
