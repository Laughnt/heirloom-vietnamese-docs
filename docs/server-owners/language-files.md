# Language Files

Heirloom bundles many locale files. Set the active locale in `config.yml`.

```yml
locale: en
```

Useful commands:

```text
/hl lang list
/hl lang missing <locale>
```

When making a custom translation, copy `lang/en.yml`, keep keys unchanged, translate only values, then run `/hl reload`.
