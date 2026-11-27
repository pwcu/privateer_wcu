#====================================
# @file   : CMakeLists.txt
# @brief  : cmake configuration file for Privateer: Wing Commander Universe (PWCU)
#====================================
# Copyright (C) 2013-2026 Rune Morling, Stephen G. Tuggy,
# Benjamen R. Meyer, and other PWCU contributors.
#
# This file is part of Privateer: Wing Commander Universe ("PWCU").
#
# PWCU is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PWCU is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PWCU.  If not, see <https://www.gnu.org/licenses/>.

CMAKE_MINIMUM_REQUIRED(VERSION 3.21 FATAL_ERROR)

SET(PWCU_VERSION_MAJOR "0")
SET(PWCU_VERSION_MINOR "9")
SET(PWCU_VERSION_PATCH "0")

# Auto-populate with the git hash of the build
IF (DEFINED ENV{SHORT_SHA} AND NOT "$ENV{SHORT_SHA}" STREQUAL "")
    SET (PWCU_VERSION_TWEAK "$ENV{SHORT_SHA}")
ELSE ()
    SET (GIT_ROOT_DIR "${CMAKE_SOURCE_DIR}")
    EXECUTE_PROCESS(
        COMMAND git rev-parse --short HEAD
        WORKING_DIRECTORY ${GIT_ROOT_DIR}
        OUTPUT_VARIABLE PWCU_VERSION_TWEAK
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
ENDIF ()

SET(PWCU_VERSION_LONG_STR "${PWCU_VERSION_MAJOR}.${PWCU_VERSION_MINOR}.${PWCU_VERSION_PATCH}-${PWCU_VERSION_TWEAK}")
SET(PWCU_VERSION_SHORT_STR "${PWCU_VERSION_MAJOR}.${PWCU_VERSION_MINOR}.${PWCU_VERSION_PATCH}")
SET(PWCU_PKG_VERSION_STR "${PWCU_VERSION_MAJOR}.${PWCU_VERSION_MINOR}.${PWCU_VERSION_PATCH}")

IF (DEFINED ENV{TAG_NAME} AND NOT "$ENV{TAG_NAME}" STREQUAL "")
    STRING(REGEX REPLACE "^v([0-9]+)\\..*" "\\1" TAG_VERSION_MAJOR "$ENV{TAG_NAME}")
    STRING(REGEX REPLACE "^v[0-9]+\\.([0-9]+).*" "\\1" TAG_VERSION_MINOR "$ENV{TAG_NAME}")
    STRING(REGEX REPLACE "^v[0-9]+\\.[0-9]+\\.([0-9]+).*" "\\1" TAG_VERSION_PATCH "$ENV{TAG_NAME}")
    STRING(REGEX REPLACE "^v[0-9]+\\.[0-9]+\\.[0-9]+(.*)" "\\1" TAG_VERSION_TWEAK "$ENV{TAG_NAME}")

    SET(TAG_VERSION_SHORT_STR "${TAG_VERSION_MAJOR}.${TAG_VERSION_MINOR}.${TAG_VERSION_PATCH}")

    IF (NOT "${PWCU_VERSION_SHORT_STR}" VERSION_EQUAL "${TAG_VERSION_SHORT_STR}")
        MESSAGE(FATAL_ERROR "Project version spelled out in CMake file does not match project version from TAG_NAME environment variable")
    ENDIF ()
    IF (NOT "${TAG_VERSION_TWEAK}" STREQUAL "")
        SET(PWCU_VERSION_LONG_STR "${PWCU_VERSION_MAJOR}.${PWCU_VERSION_MINOR}.${PWCU_VERSION_PATCH}${TAG_VERSION_TWEAK}-${PWCU_VERSION_TWEAK}")
        SET(PWCU_PKG_VERSION_STR "${PWCU_VERSION_MAJOR}.${PWCU_VERSION_MINOR}.${PWCU_VERSION_PATCH}${TAG_VERSION_TWEAK}")
    ENDIF ()
ENDIF ()

PROJECT(PWCU
    VERSION
        "${PWCU_VERSION_MAJOR}.${PWCU_VERSION_MINOR}.${PWCU_VERSION_PATCH}"
)

MESSAGE("== Privateer: Wing Commander Universe Version: ${PWCU_VERSION_LONG_STR}")

# Let cmake find our in-tree modules
SET(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${PWCU_SOURCE_DIR})

# Detect available Linux Distros that can be built for
FIND_PACKAGE(LinuxDistro REQUIRED)

INCLUDE(GNUInstallDirs)

SET(CPACK_IGNORE_FILES
    build/
    packages/
    \\\\.git/
    \\\\.vs/
    \\\\.vscode/
    ".*\\\\.pyc"
)
SET(CPACK_SOURCE_IGNORE_FILES
    build/
    packages/
    \\\\.git/
    \\\\.vs/
    \\\\.vscode/
    ".*\\\\.pyc"
)

INSTALL(DIRECTORY ai/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/ai)
INSTALL(DIRECTORY ai.easy/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/ai.easy)
INSTALL(DIRECTORY ai.hard/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/ai.hard)
INSTALL(DIRECTORY animations/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/animations)
INSTALL(DIRECTORY bases/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/bases)
INSTALL(DIRECTORY cockpits/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/cockpits)
INSTALL(DIRECTORY communications/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/communications)
INSTALL(DIRECTORY meshes/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/meshes)
INSTALL(DIRECTORY mission/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/mission)
INSTALL(DIRECTORY modules/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/modules)
INSTALL(DIRECTORY music/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/music)
INSTALL(DIRECTORY programs/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/programs)
INSTALL(DIRECTORY sectors/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/sectors)
INSTALL(DIRECTORY sounds/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/sounds)
INSTALL(DIRECTORY sprites/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/sprites)
INSTALL(DIRECTORY techniques/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/techniques)
INSTALL(DIRECTORY textures/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/textures)
INSTALL(DIRECTORY tools/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/tools)
INSTALL(DIRECTORY units/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/units)
INSTALL(DIRECTORY universe/ DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu/universe)

INSTALL(FILES
    changelog.txt
    credits.txt
    default_values_vegastrike_config.xml
    factions.xml
    find_vs_config.py
    LICENSE
    Manual.pdf
    master_part_list.csv
    master_part_list.json
    New_Game
    newsRelease.txt
    priv.icns
    pu.ico
    readme.txt
    README.md
    setup.base.xml
    setup.config
    setup.music.xml
    setup.patch.xml
    ToDo.txt
    vega.ico
    vegastrike.config
    vegastrike.xpm
    vegastrike_techniques.config
    Version.txt
    vslogo.xpm
    weapon_list.xml
    weapons.json
    DESTINATION ${CMAKE_INSTALL_DATADIR}/pwcu
)

# CPack configuration
SET(CPACK_VERBATIM_VARIABLES YES)
SET(CPACK_PACKAGE_NAME "pwcu")
SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Privateer: Wing Commander Universe mod for Vega Strike")
SET(CPACK_PACKAGE_VENDOR "Vega Strike / PWCU Team")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/README.md")
SET(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
SET(CPACK_PACKAGE_VERSION_MAJOR "${PWCU_VERSION_MAJOR}")
SET(CPACK_PACKAGE_VERSION_MINOR "${PWCU_VERSION_MINOR}")
SET(CPACK_PACKAGE_VERSION_PATCH "${PWCU_VERSION_PATCH}")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "pwcu-${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}")
SET(CPACK_CONTACT "maintainers@vega-strike.org")

# Source package filename
SET(CPACK_SOURCE_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${PWCU_PKG_VERSION_STR}-Source")
SET(CPACK_SOURCE_GENERATOR "TXZ")

IF (CMAKE_SYSTEM_NAME STREQUAL Windows)
    MESSAGE(STATUS "Configuring Packaging for Windows")
    SET(CPACK_PACKAGE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\pu.ico")
    SET(CPACK_NSIS_DISPLAY_NAME "Privateer Wing Commander Universe")
    SET(CPACK_NSIS_MANIFEST_DPI_AWARE true)
    SET(CPACK_NSIS_ENABLE_UNINSTALL_BEFORE_INSTALL YES)
    SET(CPACK_NSIS_HELP_LINK "https://vega-strike.org")
    SET(CPACK_NSIS_URL_INFO_ABOUT "https://vega-strike.org")
    SET(CPACK_NSIS_CONTACT "maintainers@vega-strike.org")
    SET(CPACK_NSIS_MODIFY_PATH OFF)
    SET(CPACK_NSIS_CREATE_ICONS_EXTRA
        "CreateShortCut '$SMPROGRAMS\\\\$STARTMENU_FOLDER\\\\Privateer Wing Commander Universe.lnk' 'C:\\\\Program Files\\\\VegaStrike-0.9\\\\bin\\\\vegastrike-engine.exe' -D\"$INSTDIR\\share\\pwcu\""
    )
    SET(CPACK_NSIS_DELETE_ICONS_EXTRA
        "Delete '$SMPROGRAMS\\\\$START_MENU\\\\Privateer Wing Commander Universe.lnk'"
    )

    SET(CPACK_GENERATOR "NSIS64")
    SET(CPACK_PACKAGE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/packages")
    SET(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${PWCU_PKG_VERSION_STR}_Windows_${CMAKE_SYSTEM_VERSION}_${CMAKE_SYSTEM_PROCESSOR}")
ELSEIF (CMAKE_SYSTEM_NAME STREQUAL Darwin)
    MESSAGE(STATUS "Configuring Packaging for macOS")
    SET(CPACK_GENERATOR "DragNDrop")
    SET(CPACK_PACKAGE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/packages")
    SET(CPACK_PACKAGE_FILE_NAME "${CPACK_PACKAGE_NAME}_${PWCU_PKG_VERSION_STR}_macOS_${CMAKE_SYSTEM_VERSION}_${CMAKE_SYSTEM_PROCESSOR}")
ELSEIF (CMAKE_SYSTEM_NAME STREQUAL Linux)
    MESSAGE(STATUS "Configuring Packaging for Linux")
    SET(CPACK_GENERATOR "TXZ")

    # "DEB"
    IF (VS_CAN_BUILD_DEB)
        MESSAGE(STATUS "Configuring Debian Packaging")
        SET(CPACK_DEBIAN_PACKAGE_NAME "pwcu")
        SET(CPACK_DEBIAN_PACKAGE_MAINTAINER "maintainers@vega-strike.org")
        SET(CPACK_DEBIAN_COMPRESSION_TYPE "bzip2")
        SET(CPACK_DEBIAN_PACKAGE_DEPENDS "vega-strike")

        SET(CPACK_PACKAGE_FILE_NAME "${CPACK_DEBIAN_PACKAGE_NAME}_${PWCU_PKG_VERSION_STR}")

        SET(CPACK_DEBIAN_PACKAGE_SECTION "Amusements/Games")
        SET(CPACK_DEBIAN_PACKAGE_HOMEPAGE "https://www.vega-strike.org")
        SET(CPACK_GENERATOR "DEB")
    ENDIF ()

    #  "RPM"
    IF (VS_CAN_BUILD_RPM)
        MESSAGE(STATUS "Configuring RPM Packaging")
        SET(CPACK_RPM_PACKAGE_LICENSE "GPLv2")
        SET(CPACK_RPM_PACKAGE_URL "https://www.vega-strike.org")
        SET(CPACK_RPM_PACKAGE_NAME "pwcu")
        SET(CPACK_RPM_PACKAGE_REQUIRES "Vega-Strike")

        # Figure out the filename
        IF (LINUX_CODENAME)
            SET(PWCU_LINUX_VERSION_STR "${LINUX_CODENAME}")
        ELSE (LINUX_CODENAME)
            SET(PWCU_LINUX_VERSION_STR "${LINUX_VERSION_ID}")
        ENDIF (LINUX_CODENAME)

        SET(CPACK_PACKAGE_FILE_NAME "${CPACK_RPM_PACKAGE_NAME}_${PWCU_PKG_VERSION_STR}-${LINUX_ID}-${PWCU_LINUX_VERSION_STR}")
        SET(CPACK_GENERATOR "RPM")
    ENDIF ()
ELSE ()
    MESSAGE(STATUS "Configuring Packaging for Unknown Platform - \"${CMAKE_SYSTEM_NAME}\"")
    SET(CPACK_GENERATOR "TXZ")
ENDIF ()

INCLUDE(CPack)
