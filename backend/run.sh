#!/bin/bash
DATABASE_URL="sqlite:////Users/ridhimajoshi/projects/devbin/data/devbin.db" python3 -m uvicorn main:app --port 8000