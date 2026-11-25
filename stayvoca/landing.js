// 언어 메뉴는 바깥을 누르거나 Esc를 누르면 닫는다
const lang = document.querySelector('.lang');
addEventListener('click', (e) => lang.contains(e.target) || lang.removeAttribute('open'));
addEventListener('keydown', (e) => e.key === 'Escape' && lang.removeAttribute('open'));

// 스크롤 장면. 장면(.scene)마다 진행도 --p(0–1)와 단계 data-step을 넣는다. 움직임은 전부 landing.css가 --p로 계산한다.
// "동작 줄이기"가 켜져 있으면 아무것도 하지 않아, 장면이 다 그려진 모습으로 차례로 놓인다
if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
  // 응원 글: 글자마다 순번을 붙여 스크롤한 만큼 짙어지게 한다. 화면 읽기 프로그램은 문장을 한 번에 읽는다
  for (const h of document.querySelectorAll('.cheer h2')) {
    const text = h.textContent;
    h.setAttribute('aria-label', text);
    h.style.setProperty('--n', text.length);
    h.replaceChildren(
      ...[...text].map((ch, i) => {
        const c = Object.assign(document.createElement('span'), { className: 'c', ariaHidden: 'true', textContent: ch });
        c.style.setProperty('--i', i);
        return c;
      }),
    );
  }

  const scenes = [...document.querySelectorAll('.scene')];
  let queued = false;
  const update = () => {
    queued = false;
    const vh = innerHeight;
    for (const s of scenes) {
      const r = s.getBoundingClientRect();
      // 장면이 화면 위에 붙은 뒤로 스크롤한 만큼. 한 화면짜리 장면은 0에 머문다
      const p = r.height > vh + 1 ? Math.min(1, Math.max(0, -r.top / (r.height - vh))) : 0;
      s.style.setProperty('--p', p.toFixed(4));
      if (s.dataset.steps) s.dataset.step = Math.min(s.dataset.steps - 1, Math.floor(p * s.dataset.steps));
      if (r.top < vh * 0.55 && r.bottom > vh * 0.45) s.classList.add('on');
    }
  };
  document.documentElement.classList.add('motion');
  addEventListener('scroll', () => queued || ((queued = true), requestAnimationFrame(update)), { passive: true });
  addEventListener('resize', update);
  update();
}
