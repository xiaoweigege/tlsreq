# tlsreq

Standalone Python package at `/Users/ww/Desktop/PyCode/tlsreq`. Not part of `spider-open-api`.

## Package

- Layout: `src/tlsreq/`
- Python: local conda `spider-open-api-3.12`; CI 3.11 / 3.12 (`wreq>=0.12` needs >=3.11)
- Install: `pip install -e ".[httpx,niquests,wreq]"`（httpx/niquests extra 会装 `xutls`）
- Tests: `python -m unittest discover -s tests -v -p 'test_*.py'`
- Live peet tests: unset `TLSREQ_SKIP_LIVE`; CI sets `TLSREQ_SKIP_LIVE=1`

## API

- `Session` / `AsyncSession(backend, impersonate, proxy, extra=)`
- Backends: `curl_cffi`, `wreq`, `niquests`, `httpx`
- `chrome152` maps to curl_cffi `chrome150` / wreq `Chrome149` / utls `chrome:152`
- `extra=` is backend-specific kwargs only
- Do not migrate `get_abck_*` into this package

## Chrome 152 / utls

- Use PyPI `xutls>=2026.9.7` (import remains `utls`). Do not install official `utls` alongside it
- Wheel `__version__` may still say 2026.7.8; check `importlib.metadata.version("xutls")`

## Publish

- GitHub: https://github.com/xiaoweigege/tlsreq
- PyPI: https://pypi.org/project/tlsreq/ (0.1.0, 0.1.1, 0.1.2, 0.1.3, 0.1.4)
- Version is `0.1.4` in `pyproject.toml` and `src/tlsreq/__init__.py`
- Publish workflow: GitHub Environment `PYPI_API_TOKEN`, secret `__TOKEN__` (not a repo secret)
- Twine user is literal `__token__`; `twine upload dist/* --non-interactive --verbose --skip-existing`
- Auto-publish on GitHub Release; bump version before a new upload
- Never commit tokens or `~/.pypirc`

## Talk

- Reply in 简体中文
