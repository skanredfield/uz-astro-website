#!/bin/sh
cd /home/skandar/projects/uz-astro-website/astrosite/astrosite/tools
echo "Last reboot time: $(date)" >> reboot_info.txt
nohup ./run_scraper_bg.sh
