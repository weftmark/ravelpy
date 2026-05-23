# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.4] - 2026-05-23

### Removed

- `Colorways.get_photo()` and `AsyncColorways.get_photo()` — the Ravelry API
  silently ignores the `colorway_id` query parameter on
  `GET /projects/search.json`, returning the same top project photo for the
  yarn regardless of which colorway is requested. No colorway-specific photo
  endpoint exists in the public API. `client.colorways` is retained as an
  empty namespace for future helpers. ([#12](https://github.com/weftmark/ravelpy/issues/12))

## [0.2.3] - 2026-05-22

### Fixed

- `get_photo()` always returned `None` because it read `first_photo` from the
  response root. The field is actually nested inside `projects[0]` in the
  `GET /projects/search.json` response. ([#10](https://github.com/weftmark/ravelpy/issues/10))

### Changed

- `ColorwayPhoto` model expanded with the full set of fields returned by the
  live API: `id`, `sort_order`, `user_id`, `x_offset`, `y_offset`,
  `medium_url`, `medium2_url`, `small2_url`, `caption`, `caption_html`,
  `copyright_holder`, `aspect_ratio`.

## [0.2.2] - 2026-05-22

### Added

- `client.colorways.get_photo(yarn_id, colorway_id)` — returns a
  `ColorwayPhoto` with `square_url`, `thumbnail_url`, and `small_url` by
  querying the projects search endpoint. Returns `None` when no user has
  photographed the colorway. ([#8](https://github.com/weftmark/ravelpy/issues/8))
- `ColorwayPhoto` model added to `ravelpy.models` and public exports.
- `AsyncColorways.get_photo()` — async equivalent.

## [0.2.1] - 2026-05-22

### Fixed

- `Colorway` model was missing `current_status` (active/discontinued flag) and
  `photos` fields; `photo_url: str` was incorrect — the API returns a list of
  photo objects, not a single URL string. ([#6](https://github.com/weftmark/ravelpy/issues/6))

### Added

- `Colorway.current_status: Optional[str]` — `None` for active colorways,
  `"discontinued"` for discontinued ones.
- `Colorway.photos: list[ColorwayPhoto]` — replaces the incorrect `photo_url`.
- `yarns.show(include="colorways")` documented with field table and examples.

## [0.2.0] - 2026-05-22

### Added

- `AsyncRavelryClient` — async equivalent of `RavelryClient` using
  `httpx.AsyncClient`. Supports context manager (`async with`) and all 38
  resource sub-clients. ([#4](https://github.com/weftmark/ravelpy/issues/4))
- `AsyncOAuthClient` — async `exchange_code()` and `refresh()` methods.
- `AsyncRavelryClient.from_oauth_token(access_token)` class method for OAuth
  Bearer token auth.

## [0.1.1] - 2026-05-22

### Fixed

- `Pack` model was missing `skeins`, `total_yards`, `total_meters`,
  `total_grams`, `total_ounces`, `yards_per_skein`, `grams_per_skein`,
  `quantity_description`, `shop_name`, and `shop_id` fields.
  ([#3](https://github.com/weftmark/ravelpy/issues/3))
- `Stash.total_skeins` property added — sums `skeins` across primary packs.
  The API's own `total_skeins` field is `null` for thread and cone-weight
  yarns; use this property instead.

## [0.1.0] - 2026-05-21

### Added

- Initial release.
- Synchronous `RavelryClient` with 38 resource sub-clients covering patterns,
  yarns, stash, queue, projects, favorites, forums, messages, shops, and more.
- Pydantic v2 models for all API response types.
- `(parsed, etag, raw)` 3-tuple return from every resource method.
- Basic Auth (read-only key) and OAuth 2.0 Bearer token support.
- `OAuthClient` for authorization code exchange and token refresh.
- Sphinx documentation published to Read the Docs.

[Unreleased]: https://github.com/weftmark/ravelpy/compare/v0.2.4...HEAD
[0.2.4]: https://github.com/weftmark/ravelpy/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/weftmark/ravelpy/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/weftmark/ravelpy/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/weftmark/ravelpy/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/weftmark/ravelpy/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/weftmark/ravelpy/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/weftmark/ravelpy/releases/tag/v0.1.0
