# StatusBarExtended

Extends the status bar in fman to show additional information.

Turn the plugin on or off by using the keyboard shortcut, default is **F3**.



**Features**

Adds extra information to the status bar.

- Show the number of directories/files and the total size of files in the current directory for both panes
- Show "Toggle hidden files" status (`◻` shown `◼` hidden)
- Show the number of selected directories/files and the total size of selected files
- Show the currently active pane indicator (`◧` left `◨` right)



**Preview**

|       Status Bar without selection       |        Status Bar with selection         |
| :--------------------------------------: | :--------------------------------------: |
| ![Screenshot macOS 10 v0.2.1](fman-plugin-statusbarextended-v0.2.1.png) | ![Screenshot macOS 10 v0.2.1-selection](fman-plugin-statusbarextended-select-v0.2.1.png) |


__Known issues__

- Alignment of indicators only works for monospaced (fixed-width) fonts since it's currently implemented using regular spaces (tip: you can change this font in a theme)
- Status bar is NOT updated when moving to another pane (only when path is changed within the active pane) since plugins can't notice a pane switch due to a lack of the [necessary APIs](https://github.com/fman-users/fman/issues/292#issuecomment-360036718)

**Changelog**

**v0.2.1 - 5.08.2021:**

- Changed the currently active pane indicator from `Pane: Left`/`Pane: Right` to `◧`/`◨` 
- Aligned the `Dirs:`/`Files:` indicators with and without selection

**v0.2.0 - 5.08.2021:**

- Works again with the latest fman version (`1.7.3`) and its new file system API ([blog](https://fman.io/blog/fmans-new-file-system-api/), [API](https://fman.io/docs/api#FileSystem))

**v0.1.2 - 15.08.2017:**

- Shorter size indicators with lower-case for (kilo)bytes: `b, k, M, G, T`. Kibibyte (`2^10`) format is preserved
- Change the status icon of hidden files toggle to `◻`white (hidden files shown) and `◼`black (hidden files hidden) Unicode square symbols
- Align all indicator position to keep it the same regardless of the length of the indicator (file/folder count is consistent up to `9,999`)
- Remove empty folder/file numbers indicators (including labels)
![Toolbar only screenshot with a custom theme v0.1.1f](fman-plugin-StatusBarExtendedF.png)
- Add thousands separator (`,`) to file/folder numbers (e.g. `Files: 1,000`)
- Change status of selected items to be consistent with the regular view for faster read

**v0.1.1 - 06.04.2017:**

- Show binary prefix instead of decimal for file size

**v0.1.0 - 01.03.2017:**

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
