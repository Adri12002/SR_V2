#!/bin/bash

# Installation des navigateurs Playwright avec toutes les dépendances système
echo ">>> Installation de Playwright et des navigateurs..."
playwright install chromium --with-deps
