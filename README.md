# Ichiran

Ichiran is a collection of tools for working with text in Japanese language. It contains experimental segmenting and romanization algorithms and uses open source [JMdictDB](http://edrdg.org/~smg/) dictionary database to display meanings of words.

The web interface is under development right now. You can try it at [ichi.moe](http://ichi.moe).

## Installation

**!!!NEW!!!** There's now a [blog post](https://readevalprint.tumblr.com/post/639359547843215360/ichiranhome-2021-the-ultimate-guide) which contains detailed instructions how to get Ichiran running on Linux and Windows. It also describes how to use the new `ichiran-cli` command line interface!

1. Download JMDict data from [here](https://gitlab.com/yamagoya/jmdictdb/-/tree/master/jmdictdb/data). If you want to initialize database from scratch download [JMDict](ftp://ftp.monash.edu.au/pub/nihongo/JMdict.gz), and optionally [kanjidic2.xml](http://www.csse.monash.edu.au/~jwb/kanjidic2/kanjidic2.xml.gz) to use ichiran/kanji functionality.
2. Create a settings.lisp file based on the provided settings.lisp.template file with the correct paths to the abovementioned files and the database connection parameters.
3. The code can be loaded as a regular ASDF system. Use quicklisp to easily install all the dependencies.
4. - Easy mode: Use database dump from [the release page](https://github.com/tshatrov/ichiran/releases) to create a suitable database. Make sure `settings.lisp` contains the correct connection parameters. Use `(ichiran/maintenance:add-errata)` to make database up to date.
   - Hard mode: Use `(ichiran/maintenance:full-init)` to completely initialize the database. Use `(ichiran/maintenance:load-jmdict)` followed by `(ichiran/maintenance:load-best-readings)` to initialize only `ichiran/dict` and not `ichiran/kanji`. Either way, this will take a few hours or so.
5. Use `(ichiran/test:run-all-tests)` to check that the installation satisfies the tests.
6. Before using any word segmenting functionality, run `(ichiran/dict:init-suffixes t)` to create a suffix cache, which will improve the quality of segmentation.

## Dockerized version

Build (executed from the root of this repo):

```
docker compose build
```

Start containers (this will take longer for the first time, because the db will get imported from the dump here, and other ichiran initializations will also get done here):

```
docker compose up
```

This will likely take several minutes, and may print a few warnings about pre-existing tables or WAL (write-ahead log) or vacuum tasks, which are safe to ignore. You may monitor the size of the database in another terminal via `du -h -d0 docker/pgdata` as it grows to around 4.7 GB. Eventually, the database will be fully restored and the `ichiran` container will start and say, "All set, awaiting commands."

If there were errors while importing db, or you want to import a new database you need to delete postgres data, so the postgres docker initdb scripts get called (if the folder is not empty it won't get called), and after this you can call `docker compose up` again:

```
sudo rm -rf docker/pgdata
```

Test suite:

```
$ docker exec -it ichiran-main-1 test-suite
This is SBCL 2.2.4, an implementation of ANSI Common Lisp.
More information about SBCL is available at <http://www.sbcl.org/>.

SBCL is free software, provided as is, with absolutely no warranty.
It is mostly in the public domain; some portions are provided under
BSD-style licenses.  See the CREDITS and COPYING files in the
distribution for more information.
......................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
Unit Test Summary
 | 748 assertions total
 | 748 passed
 | 0 failed
 | 0 execution errors
 | 0 missing tests
```

Enter the sbcl interpreter (with ichiran already initialized):

```
$ docker exec -it ichiran-main-1 ichiran-sbcl
This is SBCL 2.2.4, an implementation of ANSI Common Lisp.
More information about SBCL is available at <http://www.sbcl.org/>.

SBCL is free software, provided as is, with absolutely no warranty.
It is mostly in the public domain; some portions are provided under
BSD-style licenses.  See the CREDITS and COPYING files in the
distribution for more information.
* (romanize "一覧は最高だぞ" :with-info t)
"ichiran wa saikō da zo"
(("ichiran" . "一覧 【いちらん】
1. [n,vs] look; glance; sight; inspection
2. [n] summary; list; table; catalog; catalogue")
 ("wa" . "は
1. [prt] 《pronounced わ in modern Japanese》 indicates sentence topic
2. [prt] indicates contrast with another option (stated or unstated)
3. [prt] adds emphasis")
 ("saikō" . "最高 【さいこう】
1. [adj-no,adj-na,n] best; supreme; wonderful; finest
2. [n,adj-na,adj-no] highest; maximum; most; uppermost; supreme")
 ("da" . "だ
1. [cop,cop-da] 《plain copula》 be; is
2. [aux-v] 《た after certain verb forms; indicates past or completed action》 did; (have) done
3. [aux-v] 《indicates light imperative》 please; do")
 ("zo" . "ぞ
1. [prt] 《used at sentence end》 adds force or indicates command"))
* (ichiran:romanize "一覧は最高だぞ" :with-info t)
"ichiran wa saikō da zo"
(("ichiran" . "一覧 【いちらん】
1. [n,vs] look; glance; sight; inspection
2. [n] summary; list; table; catalog; catalogue")
 ("wa" . "は
1. [prt] 《pronounced わ in modern Japanese》 indicates sentence topic
2. [prt] indicates contrast with another option (stated or unstated)
3. [prt] adds emphasis")
 ("saikō" . "最高 【さいこう】
1. [adj-no,adj-na,n] best; supreme; wonderful; finest
2. [n,adj-na,adj-no] highest; maximum; most; uppermost; supreme")
 ("da" . "だ
1. [cop,cop-da] 《plain copula》 be; is
2. [aux-v] 《た after certain verb forms; indicates past or completed action》 did; (have) done
3. [aux-v] 《indicates light imperative》 please; do")
 ("zo" . "ぞ
1. [prt] 《used at sentence end》 adds force or indicates command"))
*
```

Ichiran cli:

```
$ docker exec -it ichiran-main-1 ichiran-cli -i "一覧は最高だぞ"
ichiran wa saikō da zo

* ichiran  一覧 【いちらん】
1. [n,vs] look; glance; sight; inspection
2. [n] summary; list; table; catalog; catalogue

* wa  は
1. [prt] 《pronounced わ in modern Japanese》 indicates sentence topic
2. [prt] indicates contrast with another option (stated or unstated)
3. [prt] adds emphasis

* saikō  最高 【さいこう】
1. [adj-no,adj-na,n] best; supreme; wonderful; finest
2. [n,adj-na,adj-no] highest; maximum; most; uppermost; supreme

* da  だ
1. [cop,cop-da] 《plain copula》 be; is
2. [aux-v] 《た after certain verb forms; indicates past or completed action》 did; (have) done
3. [aux-v] 《indicates light imperative》 please; do

* zo  ぞ
1. [prt] 《used at sentence end》 adds force or indicates command
```

### Flask API Wrapper

The Docker container includes a Flask API wrapper that exposes Ichiran functionality via HTTP REST API on port 5900 at `/i-api/v1`.

**Starting the API:**

The Flask API starts automatically when you run:

```bash
docker compose up
```

**API Endpoints:**

- **Health Check:** `GET /i-api/v1/health`
- **Analyze Text:** `GET /i-api/v1?text=<japanese_text>&format=<format>` or `POST /i-api/v1` with JSON body

**Format Options:**

- `simple` (default): Human-readable text output with romaji and word-by-word breakdown
- `full`: Structured JSON with detailed linguistic data (readings, scores, glosses, parts of speech)

**Examples:**

```bash
# Health check
curl http://localhost:5900/i-api/v1/health

# Analyze text (GET request, simple format)
curl "http://localhost:5900/i-api/v1?text=一覧は最高だぞ"

# Analyze text (POST request, simple format)
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ"}'

# Get structured JSON output (full format)
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ", "format": "full"}'

# Full format via GET
curl "http://localhost:5900/i-api/v1?text=一覧は最高だぞ&format=full"
```

**Response Format:**

**Simple format** (default):
```json
{
  "text": "一覧は最高だぞ",
  "format": "simple",
  "romaji": "ichiran wa saikō da zo",
  "analysis": "...",
  "full_output": "..."
}
```

**Full format** (structured linguistic data):
```json
{
  "text": "一覧は最高だぞ",
  "format": "full",
  "data": [
    [
      ["ichiran", {
        "reading": "一覧 【いちらん】",
        "text": "一覧",
        "kana": "いちらん",
        "score": 208,
        "seq": 1167180,
        "gloss": [...]
      }, []]
    ]
  ]
}
```

**Formatting Output with jq:**

For better readability, pipe the output through `jq`:

```bash
# Pretty print entire JSON with proper Unicode
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ"}' | jq '.'

# Show only romaji
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ"}' | jq -r '.romaji'

# Show romaji and analysis (raw output without quotes)
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ"}' | jq -r '.romaji, "\n", .analysis'

# Custom formatted output
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ"}' | jq -r '"Input: \(.text)\nRomaji: \(.romaji)\n\nAnalysis:\(.analysis)"'

# Get full structured data
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ", "format": "full"}' | jq '.'

# Extract specific fields from full format
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ", "format": "full"}' | jq '.data[0][0][] | [.[0], .[1].reading, .[1].kana]'
```

**Saving Output to Files:**

```bash
# Save pretty-printed JSON to file
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ"}' | jq '.' > output.json

# Save only analysis to text file
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ"}' | jq -r '.full_output' > analysis.txt

# Save full structured format to file
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ", "format": "full"}' | jq '.' > full_analysis.json

# Save custom format to file
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ"}' | jq -r '"Input: \(.text)\nRomaji: \(.romaji)\n\nAnalysis:\(.analysis)"' > result.txt

# Alternatively, use curl's -o flag to save raw response
curl -X POST http://localhost:5900/i-api/v1 \
  -H "Content-Type: application/json" \
  -d '{"text": "一覧は最高だぞ"}' \
  -o raw_output.json

# Then format it
jq '.' raw_output.json > formatted_output.json
```

**Example Output:**

Simple format response:
```json
{
  "format": "simple",
  "text": "一覧は最高だぞ",
  "romaji": "ichiran wa saikō da zo",
  "analysis": "\n* ichiran  一覧 【いちらん】\n1. [n,vs,vt] look; glance; sight...",
  "full_output": "ichiran wa saikō da zo\n\n* ichiran  一覧..."
}
```

Full format response (structured data):
```json
{
  "format": "full",
  "text": "一覧は最高だぞ",
  "data": [
    [[
      ["ichiran", {
        "text": "一覧",
        "reading": "一覧 【いちらん】",
        "kana": "いちらん",
        "score": 208,
        "seq": 1167180,
        "gloss": [
          {"pos": "[n,vs,vt]", "gloss": "look; glance; sight..."},
          {"pos": "[n]", "gloss": "summary; list; table..."}
        ],
        "conj": []
      }, []],
      ["wa", {...}, []],
      ...
    ], 591]
  ]
}
```

The Flask wrapper (`docker/ichiran-scripts/iapi.py`) provides a simple HTTP interface to `ichiran-cli`, making it easy to integrate Ichiran into web applications, microservices, or any system that can make HTTP requests.

## Documentation

There is no documentation yet. Any API is considered unstable at this point.

The basic functionality is `(ichiran:romanize "一覧は最高だぞ" :with-info t)`, but feel free to explore further.
