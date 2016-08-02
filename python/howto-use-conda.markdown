# How to use conda

##

- uninstall anaconda:

```shell
rm -rf ~/anaconda3
# remove the anaconda directory from PATH environment variable
rm -rf ~/.condarc ~/.conda ~/.continuum
```

- The conda configuration file can be used to change:
 - Where conda looks for packages
 - If and how conda uses a proxy server
 - Where conda lists known environments
 - Whether to update the bash prompt with the current activated environment name
 - Whether user-built packages should be uploaded to Anaconda.org
 - Default packages or features to include in new environments
 - And more.
- 使用 `--yes` 选项, 为执行命令后的所有提示选择"是"

## conda commands

- `conda update conda` - Anaconda update
- `conda config` - create conda configuration file(.condarc) in user's home directory
- 
