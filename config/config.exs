# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.
use Mix.Config

# General application configuration
config :prudget,
  ecto_repos: [Prudget.Repo]

# Configures the endpoint
config :prudget, PrudgetWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "nsbeFcFL9K4KlNNxyIKAQ93FEkPIr/IwxGsMYTHeWjSBuhXiYNSMsW9UG6z1D5e8",
  render_errors: [view: PrudgetWeb.ErrorView, accepts: ~w(html json)],
  pubsub: [name: Prudget.PubSub,
           adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env}.exs"
