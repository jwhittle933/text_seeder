# Text Parser + CouchDB Inserts
This module parses the texts contained in [starter](./starter) and inserts them into CouchDB as a document. The scripts in this directory will only work in the virtual environment, which uses [pipenv](https://pypi.org/project/pipenv/). To start the environment, run `pipenv shell`. Without this, several dependencies will throw errors unless you have them installed globally. To exit the shell, type `exit`. If a new dependency is needed, run `pipenv install <dep name>`, which will add it to your Pipfile.

Example execution for directory:
```bash
python3 seed_text.py \
  --dir ./starter/mt/Tanach_vow \
  --write --insert
```

The script also handles single files:
```bash
python3 seed_text.py \
  --file ./starter/mt/Tanach_vow.Joshua.txt \
  --write --insert
```

### Flags
`--dir` - Select the directory that contains valid file. Overridden by `--file`
`--file` - Select the file to parse. Overrides `--dir`
`--pattern` - Filename pattern to search. Use with `--dir`. Defaults to `*.txt*`
`--insert` - Bool flag that triggers a database insert.
`--write` - Bool flag that writes triggers json file creation


