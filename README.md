# django-ts-routes

**django-ts-routes** is a Django application allowing to expose and perform reverse lookups of Django named URL patterns in a TypeScript code base. This codebase is based on [django-js-routes](https://github.com/ellmetha/django-js-routes). Big thanks to the original author of this package.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Settings](#settings)
- [Advanced features](#advanced-features)
- [License](#license)

## Installation

To install django-ts-routes, please use the pip command as follows:

```shell
$ pip install django-ts-routes
```

Once the package is installed, you'll have to add the application to `INSTALLED_APPS` in your project's settings module:

```python
INSTALLED_APPS = (
    # all other apps...
    'ts_routes',
)
```

You can then define which URL patterns or URL namespaces you want to expose by setting the `TS_ROUTES_INCLUSION_LIST` setting (for compatibility with [django-js-routes](https://github.com/ellmetha/django-js-routes) you can also use `JS_ROUTES_INCLUSION_LIST`). This setting allows to define which URLs should be serialized and made available to the client side through the generated and / or exported TypeScript helper. This list should contain only URL pattern names or namespaces. Here is an example:

```python
TS_ROUTES_INCLUSION_LIST = [
    'home',
    'catalog:product_list',
    'catalog:product_detail',
]
```

Note that if a namespace is included in this list, all the underlying URLs will be made available to the client side through the generated TypeScript helper. Django-ts-routes is safe by design in the sense that _only_ the URLs that you configure in this inclusion list will be publicly exposed on the client side.

Once the list of URLs to expose is configured, you can dump the routes with the management command `dump_routes_resolver`:

```shell
$ python manage.py dump_routes_resolver --output-dir=static/src/routes
```

## Usage

The URL patterns you configured through the `TS_ROUTES_INCLUSION_LIST` setting will be exported to TypeScript files in the `output-dir` directory. This directory will contain a `index.ts` with routes of the default language, other supported languages will be in separate files. The files export the `reverseUrl` function that can be used to generate URLs in your TypeScript code.

```typescript
import reverseUrl from "@/routes";

reverseUrl("home");
reverseUrl("catalog:product_list");
reverseUrl("catalog:product_detail", { pk: productId });
```

## Settings

### TS_ROUTES_INCLUSION_LIST

Default: `[]`

The `TS_ROUTES_INCLUSION_LIST` setting allows to define the URL patterns and URL namespaces that should be exposed.

## License

MIT. See `LICENSE` for more details.
