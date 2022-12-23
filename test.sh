#!/bin/sh
echo "The nodes will quit in 5 minutes" & sleep 300; docker swarm leave --force