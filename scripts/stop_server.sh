#!/bin/bash
isExistApp = `pgrep httpd`
if [[ -n  $isExistApp ]]; then
    service httpd stop        
fi
rm -r /var/www/ealugame.com/*