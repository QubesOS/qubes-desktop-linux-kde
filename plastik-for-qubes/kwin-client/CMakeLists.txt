project (kwin-plastik-for-qubes)

add_subdirectory( config )

########### next target ###############

set(kwin3_plastik_for_qubes_PART_SRCS
   plastik.cpp
   plastikclient.cpp
   plastikbutton.cpp
   qubeslabels.cpp
   )

kde4_add_plugin(kwin3_plastik_for_qubes ${kwin3_plastik_for_qubes_PART_SRCS})

target_link_libraries(kwin3_plastik_for_qubes
    ${X11_LIBRARIES}
    ${KDE4_KDEUI_LIBS}
    ${KDE4WORKSPACE_KDECORATIONS_LIBS}
    kdecorations
    )

install(TARGETS kwin3_plastik_for_qubes  DESTINATION ${PLUGIN_INSTALL_DIR} )


########### install files ###############

install( FILES plastik_for_qubes.desktop  DESTINATION  ${DATA_INSTALL_DIR}/kwin/ )

