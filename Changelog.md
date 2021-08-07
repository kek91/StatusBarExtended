# Changelog
All notable changes to this project will be documented in this file

[unreleased]: https://github.com/kek91/StatusBarExtended/compare/v0.3.0...HEAD
## [Unreleased]

## [v0.3.0 — 07.08.2021]
   [v0.3.0 — 07.08.2021]: https://github.com/kek91/StatusBarExtended/releases/tag/v0.3.0
  - __Fixed__
    + :beetle: Hidden files not counted even when they're shown
    + :beetle: Not updating on pane changes via keyboard `switch_panes` command (e.g. with a <kbd>Tab</kbd>)

## [v0.2.1 — 05.08.2021]
   [v0.2.1 — 05.08.2021]: https://github.com/kek91/StatusBarExtended/releases/tag/v0.2.1
  - __Changed__
    + The currently active pane indicator from `Pane: Left`/`Pane: Right` to `◧`/`◨` 
    + The `Dirs:`/`Files:` indicators' to align with and without selection

## [v0.2.0 — 05.08.2021]
   [v0.2.0 — 05.08.2021]: https://github.com/kek91/StatusBarExtended/releases/tag/v0.2.0
  - __Fixed__
    + :beetle: Not working with the latest fman version (`1.7.3`) and its new file system API ([blog](https://fman.io/blog/fmans-new-file-system-api/), [API](https://fman.io/docs/api#FileSystem))

## [v0.1.2 — 15.08.2017]
   [v0.1.2 — 15.08.2017]: https://github.com/kek91/StatusBarExtended/releases/tag/v0.1.2
  - Shorter size indicators with lower-case for (kilo)bytes: `b, k, M, G, T`. Kibibyte (`2^10`) format is preserved
  - Change the status icon of hidden files toggle to `◻`white (hidden files shown) and `◼`black (hidden files hidden) Unicode square symbols
  - Align all indicator position to keep it the same regardless of the length of the indicator (file/folder count is consistent up to `9,999`)
  - Remove empty folder/file numbers indicators (including labels)
  ![Toolbar only screenshot with a custom theme v0.1.1f](fman-plugin-StatusBarExtendedF.png)
  - Add thousands separator (`,`) to file/folder numbers (e.g. `Files: 1,000`)
  - Change status of selected items to be consistent with the regular view for faster read

## [v0.1.1 — 06.04.2017]
   [v0.1.1 — 06.04.2017]: https://github.com/kek91/StatusBarExtended/releases/tag/v0.1.1
  - Show binary prefix instead of decimal for file size

## [v0.1.0 — 01.03.2017]
   [v0.1.0 — 01.03.2017]: https://github.com/kek91/StatusBarExtended/releases/tag/v0.1.0
  - Shows output only for the currently active pane due to layout/resize issues 
  - Don't display "Files: n" and "Size: n xB" if there are 0 files in current directory
  - Hidden status is visualized by checkmark or cross


**25.02.2017:**

  - Align text to the left and right for the respective panes
  - Reduce text to make the status bar smaller thus allowing resizing window smaller


**19.01.2017:**

  - Shows selected directores and files/filesize when selecting files
  - Restructured code for readability


**16.01.2017:**

  - StatusBar shows immediately when toggled


**28.11.2016:**

  - Cleaned code
  - Should work in all 3 supported OS (tested on Windows and Linux only)
