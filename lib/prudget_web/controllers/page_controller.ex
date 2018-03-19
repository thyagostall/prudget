defmodule PrudgetWeb.PageController do
  use PrudgetWeb, :controller

  def index(conn, _params) do
    render conn, "index.html"
  end
end
