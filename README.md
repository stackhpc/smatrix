# smatrix

Run a matrix of Slurm jobs by templating sbatch file(s).

## Example

Template sbatch file `./template.sh.j2`:

```shell
#!/usr/bin/bash
#SBATCH --job-name=test
#SBATCH --nodes={{ item.nodes }}
#SBATCH --dependency=singleton
echo myparam: {{ item.myparam }}
srun hostname
sleep 30
```

Playbook:
```yaml
- hosts: localhost
  become: no
  gather_facts: no
  vars:
    smatrix_dimensions:
      nodes: [1,2]
      myparam:
        - A
        - B
    smatrix_template_dest_dir: out
    smatrix_exclude:
      - nodes: 1
        myparam: A
  tasks:
    - import_role:
        name: smatrix
```

This role will create sbatch files in a directory `out/` (which it will create if necessary). There will be 3x templated sbatch scripts, `template.1-B.sh`, `template.2-A.sh`, and `template.2-B.sh`, one for each combination of values in dimensions, excluding the case where `nodes=1` and `myparam=A`. Within the templated files, the `{{ item.name }}` strings are replaced with the appropriate value for that run. It will then submit the sbatch scripts to slurm.

This example also demonstrates job control; because the job-name is set to a single value across all runs (by default it will be the sbatch script name) and a singleton-type dependency is declared, only a single job in this matrix will run at once.

## Role Variables

- `smatrix_template_src`: Optional. Name or path of sbatch file to template. Default `template.sh.j2`. Note that this could potentially include dimension values.
- `smatrix_template_dest_dir`: Optional. Directory to write templated sbatch files into. Default `.`
- `smatrix_dimensions`: Optional. Mapping defining dimensions for test matrix, where each key is the dimension name and each value is a list of possible values. These can be used for templating in `smatrix_template_src` using `{{ item.<dimension> }}` where `<dimension>` is a key name. Default is `{}`.
- `smatrix_exclude`: Optional. List of dimension combinations to skip. Each element should be a dict with keys and values from `smatrix_dimensions`. Default is `[]`.

### Sbatch filename control
The default is to construct the filename of the templated sbatch files from the `smatrix_template_src` basename, like: `template.sh.j2` -> `template.PARAMETERS.sh`, where `PARAMETERS` here is the run's dimension values joined with '-'. This can be overriden using the following variables:
- `smatrix_template_basename`: Optional. Base name of templated sbatch files. Default takes the 1st dotted component of `smatrix_template_src`.
- `smatrix_template_ext`: Optional. Extension to use for templated sbatch files. Default is the 2nd dotted component of `smatrix_template_src`.
- `smatrix_template_suffix`: Optional. String to use as run-specific suffix. Default is ".{{ item.values() | join('-') }}" where `item` is a dict for the run's dimension selections.
- `smatrix_template_dest`: Optional. Path to output a templated sbatch file to. Default `"{{ smatrix_template_dest_dir }}/{{ smatrix_template_basename }}{{ smatrix_template_suffix}}.{{ smatrix_template_ext}}"`.
