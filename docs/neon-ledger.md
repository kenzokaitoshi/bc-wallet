neon-wallet/
│
│
├── docs/
│   ├── neon-wallet.md
│   └── world.md
│
├── neon_wallet/
│   ├── __init__.py
│   ├── transaction/
│   │   ├── __init__.py
│   │   ├── helpres_tx.py
│   │   └── transaction.py
|   |   └── tx_in.py
|   |   └── tx_out.py
|   |   └── unspent_tx_out.py
|   |   └── transactions.py
│   │
│   └── wallet/
│       ├── __init__.py
│       ├── helpers.py
│       └── wallet.py
│
├── data/
│   ├── input.csv
│   └── output.xlsx
│
├── tests/
│   ├── transaction
│   │   ├── helpers_tests.py
│   │   └── test_transaction.py
│   ├── transaction_pool
│   │   ├── helpers_tests.py
│   │   └── test_transaction_pool.py
│   └── wallet/
│   |    ├── helpers_tests.py
│   |    └── test_wallet.py
│   └── helpers_data.py
├── .gitignore
├── LICENSE
└── README.md