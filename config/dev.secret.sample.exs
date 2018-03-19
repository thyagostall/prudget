use Mix.Config

config :prudget, Prudget.Repo,
  adapter: Ecto.Adapters.Postgres,
  username: "<<username>>",
  password: "<<password>>",
  database: "<<database name>>",
  hostname: "<<dataabse host name>>",
  pool_size: 10

config :guardian_demo, Prudget.Guardian,
  issuer: "prudget",
  secret_key: "secret key generated through `mix guardian.gen.secret`"
