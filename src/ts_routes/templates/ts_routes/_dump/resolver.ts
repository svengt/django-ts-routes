/* eslint-disable */

const routes = {{ routes|safe }} as const;

// examples:
// const routes = {
//     home: "/",
//     "books:book_detail": "/books/<int:pk>/",
//     "users:reset_password": "/users/reset-password/<uidb64>/<token>/",
// } as const;

type _UnwrapParam<
    P extends string,
    S extends string[]
> = P extends `<${infer Q}>` ? [Q, ...S] : S;

type _Match<
    T extends string,
    S extends string[]
> = T extends `${infer P}/${infer R}`
    ? _Match<R, _UnwrapParam<P, S>>
    : _UnwrapParam<T, S>;

type Match<T extends string> = _Match<T, []>[number];

type ExtractKey<T extends string> = T extends `${string}:${infer K}` ? K : T;
type ExtractType<T extends string> = T extends `int:${string}`
    ? number
    : string;
type Extractor<T extends string> = {
    [K in Match<T> as ExtractKey<K>]: ExtractType<K>;
};

export type RouteKeys = keyof typeof routes;
export type Route<T extends RouteKeys> = (typeof routes)[T];
export type RouteParams<T extends RouteKeys> = Extractor<Route<T>>;

function reverseUrl<T extends RouteKeys>(
    urlName: T,
    ...args: Record<string, never> extends RouteParams<T>
        ? [args?: never]
        : [args: RouteParams<T>]
): Route<T> {
    const url = routes[urlName];

    const argTokens = url.match(/<(\w+\:)?\w*>/g);
    if (!argTokens && args.length > 0) {
        throw (
            "Invalid URL lookup: URL '" +
            urlName +
            "' does not expect any arguments."
        );
    }

    if (argTokens) {
        return argTokens.reduce((acc, token) => {
            if (args[0] === undefined) {
                throw (
                    "Invalid URL lookup: URL '" +
                    urlName +
                    "' expects " +
                    argTokens.length +
                    " arguments."
                );
            }
            // Remove the type prefix from the token, e.g. "<int:pk>" -> "pk"
            const argName = token.slice(1, -1).replace(/^\w+\:/, "") as keyof RouteParams<T>;
            // Get the value of the argument, e.g. { pk: 1 } -> 1
            const argValue = String(args[0][argName]);
            return acc.replace(token, argValue);
        }, url) as Route<T>;
    }

    return url;
}

export default reverseUrl;
