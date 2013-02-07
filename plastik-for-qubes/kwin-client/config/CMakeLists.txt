set(kwin_plastik_for_qubes_config_PART_SRCS config.cpp )

kde4_add_ui_files(kwin_plastik_for_qubes_config_PART_SRCS configdialog.ui )

kde4_add_plugin(kwin_plastik_for_qubes_config ${kwin_plastik_for_qubes_config_PART_SRCS})

target_link_libraries(kwin_plastik_for_qubes_config ${KDE4_KDEUI_LIBS})

install(TARGETS kwin_plastik_for_qubes_config  DESTINATION ${PLUGIN_INSTALL_DIR} )
