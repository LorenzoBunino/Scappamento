# scappamento
#### B2B automation for music stores

Supported suppliers / platforms:
- [x] Yamaha
- [x] Fender
- [x] Frenexport
- [ ] Proel (WIP)
- [x] Suonostore
- [ ] MusicPool (WIP, broken)
- [ ] MEPA (WIP)

Spiritfarer is a nice game

### TODO
- [ ] Module / Package
- [ ] First release

|          :broccoli:           | yamaha             | fender             | proel              | frenexport         | suonostore         | musicpool          | mepa               | _common            |
|:-----------------------------:|:-------------------|:-------------------|:-------------------|:-------------------|:-------------------|:-------------------|:-------------------|:-------------------|
|       No write to disk        | :heavy_check_mark: | :heavy_check_mark: | :x:                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :heavy_minus_sign: |
|     Handle missing config     | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                |
|        Default config         | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :x:                |
|    Config default location    | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :heavy_minus_sign: | :x:                |
|   Description head comment    | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                | :x:                | :heavy_check_mark: | :x:                | :heavy_check_mark: |
|      Column count check       | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :heavy_minus_sign: |
|       Column name check       | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :heavy_minus_sign: |
|      Column layout check      | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :heavy_minus_sign: |
|      "Exit code" to file      | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :heavy_minus_sign: |
|        _common config         | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: | :x:                | :x:                | :x:                | :x:                | :heavy_minus_sign: |
| "final_path" to "target_path" | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :heavy_minus_sign: |
|     OS-independent paths      | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :x:                | :heavy_minus_sign: |

New commit labels: `fix`, `feat`, `test`, `refactor`, `perf`