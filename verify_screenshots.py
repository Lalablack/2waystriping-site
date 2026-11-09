#!/usr/bin/env python3
"""Take proper verification screenshots including favicon check."""

import os
from playwright.sync_api import sync_playwright

def take_screenshots(base_url, output_prefix):
    """Take screenshots at different viewports."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # Desktop screenshots (1280px wide)
        print(f"\nDesktop screenshots (1280px)...")
        ctx_desktop = browser.new_context(viewport={'width': 1280, 'height': 1024})
        page_desktop = ctx_desktop.new_page()
        page_desktop.goto(base_url, wait_until='networkidle')
        
        # Header
        header = page_desktop.locator('nav.top')
        header.screenshot(path=f'/opt/cursor/artifacts/{output_prefix}-desktop-header.png')
        print(f"  ✓ {output_prefix}-desktop-header.png")
        
        # Footer
        page_desktop.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page_desktop.wait_for_timeout(500)
        footer = page_desktop.locator('footer.ft')
        footer.screenshot(path=f'/opt/cursor/artifacts/{output_prefix}-desktop-footer.png')
        print(f"  ✓ {output_prefix}-desktop-footer.png")
        
        ctx_desktop.close()
        
        # Mobile screenshots - test multiple widths
        for width in [320, 375, 414]:
            print(f"\nMobile screenshot ({width}px)...")
            ctx_mobile = browser.new_context(viewport={'width': width, 'height': 667})
            page_mobile = ctx_mobile.new_page()
            page_mobile.goto(base_url, wait_until='networkidle')
            
            # Header
            header_mobile = page_mobile.locator('nav.top')
            header_mobile.screenshot(path=f'/opt/cursor/artifacts/{output_prefix}-mobile-{width}-header.png')
            print(f"  ✓ {output_prefix}-mobile-{width}-header.png")
            
            # Footer
            page_mobile.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page_mobile.wait_for_timeout(500)
            footer_mobile = page_mobile.locator('footer.ft')
            footer_mobile.screenshot(path=f'/opt/cursor/artifacts/{output_prefix}-mobile-{width}-footer.png')
            print(f"  ✓ {output_prefix}-mobile-{width}-footer.png")
            
            ctx_mobile.close()
        
        # Favicon verification - proper check with light and dark backgrounds
        print(f"\nFavicon verification...")
        ctx_fav = browser.new_context(viewport={'width': 1000, 'height': 600})
        page_fav = ctx_fav.new_page()
        
        favicon_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="icon" href="{base_url}/images/favicon-32.png" type="image/png">
            <style>
                body {{ margin: 30px; background: #f0f0f0; font-family: -apple-system, system-ui, sans-serif; font-size: 13px; }}
                .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
                .box {{ background: white; padding: 24px; border: 1px solid #ddd; border-radius: 4px; text-align: center; }}
                .box.dark {{ background: #1a1a1a; color: #fff; }}
                .box.tab {{ background: #e8eaed; padding: 12px 16px; border-radius: 8px 8px 0 0; display: inline-flex; align-items: center; gap: 8px; }}
                .fav-display {{ display: inline-block; }}
                img {{ display: block; image-rendering: -webkit-optimize-contrast; }}
                .label {{ margin-top: 16px; color: #666; font-weight: 500; }}
                .box.dark .label {{ color: #999; }}
                h2 {{ margin: 0 0 20px; font-size: 18px; font-weight: 600; }}
                .pixel-size {{ font-size: 11px; color: #999; margin-top: 8px; }}
            </style>
        </head>
        <body>
            <h2>Favicon Verification: 2 Way Striping Logo</h2>
            
            <div class="grid">
                <div class="box">
                    <div class="fav-display">
                        <img src="{base_url}/images/favicon-16.png" width="16" height="16" alt="16x16">
                    </div>
                    <div class="label">16×16 actual size</div>
                    <div class="pixel-size">Light background</div>
                </div>
                
                <div class="box">
                    <div class="fav-display">
                        <img src="{base_url}/images/favicon-32.png" width="32" height="32" alt="32x32">
                    </div>
                    <div class="label">32×32 actual size</div>
                    <div class="pixel-size">Light background</div>
                </div>
                
                <div class="box">
                    <div class="fav-display">
                        <img src="{base_url}/images/favicon-32.png" width="64" height="64" alt="32x32 enlarged">
                    </div>
                    <div class="label">32×32 enlarged 2x</div>
                    <div class="pixel-size">For inspection</div>
                </div>
                
                <div class="box dark">
                    <div class="fav-display">
                        <img src="{base_url}/images/favicon-16.png" width="16" height="16" alt="16x16 dark">
                    </div>
                    <div class="label">16×16 actual size</div>
                    <div class="pixel-size">Dark background</div>
                </div>
                
                <div class="box dark">
                    <div class="fav-display">
                        <img src="{base_url}/images/favicon-32.png" width="32" height="32" alt="32x32 dark">
                    </div>
                    <div class="label">32×32 actual size</div>
                    <div class="pixel-size">Dark background</div>
                </div>
                
                <div class="box">
                    <div class="box tab">
                        <img src="{base_url}/images/favicon-16.png" width="16" height="16" alt="tab">
                        <span style="color: #202124;">2waystriping.com</span>
                    </div>
                    <div class="label">Browser tab simulation</div>
                    <div class="pixel-size">16×16 in context</div>
                </div>
            </div>
        </body>
        </html>
        """
        
        page_fav.goto(f"data:text/html,{favicon_html}")
        page_fav.wait_for_timeout(800)
        page_fav.screenshot(path=f'/opt/cursor/artifacts/{output_prefix}-favicon-check.png')
        print(f"  ✓ {output_prefix}-favicon-check.png")
        
        ctx_fav.close()
        browser.close()
    
    print(f"\n✅ All screenshots saved")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: verify_screenshots.py <base_url> <prefix>")
        sys.exit(1)
    take_screenshots(sys.argv[1], sys.argv[2])
