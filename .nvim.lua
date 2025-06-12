vim.lsp.config('ty', {
  cmd = { "uv", "run", "ty", "server" },
  filetypes = { "python" },
  init_options = {
    settings = {
      experimental = {
        completions = {
          enable = true
        }
      },

      trace = {
        server = "messages"
      }
    }
  }
})
vim.lsp.config('ruff', {
  cmd = { "uv", "run", "ruff", "server" },
  filetypes = { "python" },
})

-- Required: Enable the language server
vim.lsp.enable('ruff')
vim.lsp.enable('ty')
