#!/usr/bin/env python3
"""Take before/after screenshots of the 2waystriping.com site."""

import os
import sys
from playwright.sync_api import sync_playwright

def take_screenshots(base_url, output_prefix):
    """Take screenshots at different viewports."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Desktop screenshots (1280px wide)
        print(f"\nTaking desktop screenshots ({output_prefix})...")
        context_desktop = browser.new_context(viewport={'width': 1280, 'height': 1024})
        page_desktop = context_desktop.new_page()
        
        # Load the page
        page_desktop.goto(base_url, wait_until='networkidle')
        
        # Header screenshot
        header = page_desktop.locator('nav.top')
        header.screenshot(path=f'/workspace/{output_prefix}-desktop-header.png')
        print(f"  ✓ {output_prefix}-desktop-header.png")
        
        # Footer screenshot - scroll to bottom first
        page_desktop.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page_desktop.wait_for_timeout(500)
        footer = page_desktop.locator('footer.ft')
        footer.screenshot(path=f'/workspace/{output_prefix}-desktop-footer.png')
        print(f"  ✓ {output_prefix}-desktop-footer.png")
        
        # Full page screenshot (optional, might be large)
        # page_desktop.screenshot(path=f'/workspace/{output_prefix}-desktop-full.png', full_page=True)
        
        context_desktop.close()
        
        # Mobile screenshots (375px wide)
        print(f"\nTaking mobile screenshots ({output_prefix})...")
        context_mobile = browser.new_context(viewport={'width': 375, 'height': 667})
        page_mobile = context_mobile.new_page()
        
        # Load the page
        page_mobile.goto(base_url, wait_until='networkidle')
        
        # Header screenshot
        header_mobile = page_mobile.locator('nav.top')
        header_mobile.screenshot(path=f'/workspace/{output_prefix}-mobile-header.png')
        print(f"  ✓ {output_prefix}-mobile-header.png")
        
        # Footer screenshot
        page_mobile.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page_mobile.wait_for_timeout(500)
        footer_mobile = page_mobile.locator('footer.ft')
        footer_mobile.screenshot(path=f'/workspace/{output_prefix}-mobile-footer.png')
        print(f"  ✓ {output_prefix}-mobile-footer.png")
        
        context_mobile.close()
        
        # Favicon check - take a screenshot of just the favicon area
        print(f"\nTaking favicon screenshot ({output_prefix})...")
        context_fav = browser.new_context(viewport={'width': 800, 'height': 600})
        page_fav = context_fav.new_page()
        
        # Create a simple HTML page that shows the favicon large
        favicon_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="icon" href="{base_url}/images/2way-favicon.png" type="image/png">
            <style>
                body {{ margin: 40px; background: #f5f5f5; font-family: sans-serif; }}
                .box {{ background: white; padding: 30px; border: 1px solid #ddd; display: inline-block; }}
                img {{ display: block; image-rendering: pixelated; }}
                .label {{ margin-top: 20px; font-size: 14px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="box">
                <img src="{base_url}/images/2way-favicon.png" width="32" height="32" alt="Favicon at 32px">
                <div class="label">Favicon at 32×32 actual size</div>
            </div>
            <div class="box" style="margin-left: 20px;">
                <img src="{base_url}/images/2way-favicon.png" width="64" height="64" alt="Favicon at 64px">
                <div class="label">Favicon scaled to 64×64 for visibility</div>
            </div>
        </body>
        </html>
        """
        
        page_fav.goto(f"data:text/html,{favicon_html}")
        page_fav.wait_for_timeout(500)
        page_fav.screenshot(path=f'/workspace/{output_prefix}-favicon-check.png')
        print(f"  ✓ {output_prefix}-favicon-check.png")
        
        context_fav.close()
        browser.close()
    
    print(f"\n✅ All screenshots saved for {output_prefix}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: take_screenshots.py <base_url> <output_prefix>")
        sys.exit(1)
    
    take_screenshots(sys.argv[1], sys.argv[2])
