from anima_vis_forestsim import __version__, get_device_info, load_settings


def test_import_surface_exposes_expected_symbols() -> None:
    assert __version__ == "0.1.0"
    assert callable(load_settings)
    info = get_device_info()
    assert info.backend in {"mlx", "cuda", "cpu"}
