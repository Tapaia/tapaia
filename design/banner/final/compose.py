"""Compose the final header (scene + coin-as-sun lockup, wordmark CSS unchanged) and the X-profile preview."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'styles'))
import compose_styles as cs  # noqa: E402  (same relative depth: ../../logo, ../../mockups-v2)

SLUG = 'tapaia-x-header'
cs.STYLES['FINAL'] = dict(cs.STYLES['A'], slug=SLUG, name='Golden Hour (style A, final)', bg='art/scene-750x250.png')

if __name__ == '__main__':
    open(f'{HERE}/{SLUG}.html', 'w').write(cs.banner_html('FINAL'))
    open(f'{HERE}/{SLUG}-preview.html', 'w').write(cs.preview_html('FINAL'))
    print('html ok')
