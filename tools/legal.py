"""Legal pages: /terms/ (terms of service, payment & work conditions) and /privacy/ (privacy policy).

Written in en, de, ru; every other language links to the English version.
Data below is plain text: each section is (heading, [paragraphs]).
TODO for the owner: legal entity name and postal address (Impressum) — fill COMPANY when known.
"""
import os, datetime
import news

e = news.e
BASE = news.BASE
UPDATED = "2026-11-24"
COMPANY = {"name": "VA Corporation", "address": None}  # address pending: added once the owner provides it
CONTACT = "WhatsApp / Telegram +34 641 387 122 · https://wa.me/34641387122 · https://t.me/vladimiramelchenko33"

TITLES = {
 "terms": {"en": "Terms of service, payment and work conditions", "de": "AGB: Leistungs-, Zahlungs- und Arbeitsbedingungen", "ru": "Условия работы, оплаты и обслуживания"},
 "privacy": {"en": "Privacy policy", "de": "Datenschutzerklärung", "ru": "Политика конфиденциальности"},
}
UI = {"en": ("Last updated", "Legal", "Terms", "Privacy"), "de": ("Stand", "Rechtliches", "AGB", "Datenschutz"), "ru": ("Обновлено", "Правовая информация", "Условия", "Конфиденциальность")}

TERMS = {
"en": [
 ("1. Scope", ["These terms apply to all services of VA Corporation: AI agents, automation, AI-powered SMM and video, Telegram bots, websites, dashboards and games. Anything agreed individually in writing (a message or e-mail is enough) takes priority over these terms."]),
 ("2. Prices", ["All prices on the website are starting prices in euro and do not include VAT; VAT is added where the law requires it. The exact price is fixed in a written quote after a short free consultation, based on the scope of the project.",
   "Monthly maintenance and support are not included in the one-time price. Their cost depends on the complexity of the project and is agreed in the quote. Third-party costs (AI model usage, hosting, domains, paid APIs, app-store or advertising fees) are paid by the client directly or re-invoiced at cost, unless agreed otherwise."]),
 ("3. How a project runs", ["1) Free consultation — we clarify the goal. 2) Written quote with scope, price, stages and deadlines. 3) Prepayment and start. 4) Prototype or first version for your feedback. 5) Revisions, final delivery and launch. 6) Optional maintenance.",
   "Deadlines start when the prepayment and all materials and access we need from you (texts, logos, accounts, data) have been received. Delays caused by missing materials or feedback move the deadlines accordingly."]),
 ("4. Payment", ["One-time projects: 50 % prepayment before work starts and 50 % on delivery, before the final handover or launch. Projects above €3,000 can be split into stages (for example 40 % / 30 % / 30 %).",
   "Monthly services (AI SMM packages, maintenance, hosting of agents): paid monthly in advance. The minimum term is one month; you can cancel at any time with effect from the end of the paid month.",
   "Invoices are payable within 7 days by bank transfer or another method stated on the invoice. If payment is late we may pause the work or the service until it is received."]),
 ("5. Revisions and acceptance", ["Each quote includes up to two rounds of revisions within the agreed scope. New features or changes to the agreed scope are quoted separately.",
   "The result is considered accepted when you confirm it or start using it, or 7 days after delivery if no substantiated defects are reported."]),
 ("6. Warranty and support", ["We fix errors in our own work that are reported within 30 days after delivery free of charge. This does not cover changes made by third parties, changes of external services (for example new rules or APIs of Instagram, TikTok, Telegram or AI providers) or new requirements.",
   "AI agents work with probabilistic models: they can make mistakes. We configure them carefully and test them with you, but the client remains responsible for checking important answers and for how the agent is used in their business."]),
 ("7. Rights to the results", ["After full payment you receive the right to use the delivered results (texts, designs, videos, code) for your business without limits in time or territory. We may show the project in our portfolio unless you ask us not to. Third-party components (open-source libraries, fonts, stock media, AI models) remain under their own licences."]),
 ("8. Client responsibilities", ["You make sure that the materials you provide do not infringe the rights of others and that the use of the agent or content complies with the laws and platform rules that apply to your business (advertising, data protection, consumer law)."]),
 ("9. Liability", ["We are liable without limitation for intent and gross negligence. In all other cases our liability is limited to the amount paid for the affected service; liability for lost profit and indirect damage is excluded as far as the law allows. Mandatory consumer rights remain unaffected."]),
 ("10. Cancellation", ["You can stop a one-time project at any time. Work already done up to that moment is paid; the prepayment is set off against it and any rest is refunded.",
   "If you are a consumer in the EU, you have a 14-day right of withdrawal for contracts concluded at a distance. If you ask us to start the work within these 14 days, you pay for the part already done if you withdraw; the right expires once the service has been fully performed."]),
 ("11. Final provisions", ["If a provision of these terms is invalid, the rest remains valid. Questions about these terms: " + CONTACT + "."]),
],
"de": [
 ("1. Geltungsbereich", ["Diese Bedingungen gelten für alle Leistungen von VA Corporation: KI-Agenten, Automatisierung, SMM und Videos mit KI, Telegram-Bots, Websites, Dashboards und Spiele. Individuelle Vereinbarungen in Textform (eine Nachricht oder E-Mail genügt) haben Vorrang."]),
 ("2. Preise", ["Alle Preise auf der Website sind Einstiegspreise in Euro zuzüglich der gesetzlichen Mehrwertsteuer, soweit diese anfällt. Der genaue Preis wird nach einer kurzen kostenlosen Beratung in einem schriftlichen Angebot je nach Projektumfang festgelegt.",
   "Die monatliche Wartung und Betreuung ist im Einmalpreis nicht enthalten. Ihre Kosten hängen von der Komplexität des Projekts ab und werden im Angebot vereinbart. Kosten Dritter (Nutzung von KI-Modellen, Hosting, Domains, kostenpflichtige APIs, App-Store- oder Werbegebühren) trägt der Kunde direkt oder sie werden zum Selbstkostenpreis weiterberechnet, sofern nichts anderes vereinbart ist."]),
 ("3. Projektablauf", ["1) Kostenlose Beratung — wir klären das Ziel. 2) Schriftliches Angebot mit Umfang, Preis, Phasen und Terminen. 3) Anzahlung und Start. 4) Prototyp oder erste Version für Ihr Feedback. 5) Korrekturen, Abnahme und Launch. 6) Optionale Betreuung.",
   "Fristen beginnen, sobald die Anzahlung sowie alle benötigten Materialien und Zugänge (Texte, Logos, Konten, Daten) vorliegen. Verzögerungen durch fehlende Materialien oder Rückmeldungen verschieben die Termine entsprechend."]),
 ("4. Zahlung", ["Einmalige Projekte: 50 % Anzahlung vor Arbeitsbeginn und 50 % bei Lieferung, vor der finalen Übergabe bzw. dem Launch. Projekte über 3.000 € können in Etappen aufgeteilt werden (z. B. 40 % / 30 % / 30 %).",
   "Monatliche Leistungen (KI-SMM-Pakete, Wartung, Betrieb von Agenten): monatlich im Voraus. Mindestlaufzeit ein Monat; Kündigung jederzeit zum Ende des bezahlten Monats.",
   "Rechnungen sind innerhalb von 7 Tagen per Überweisung oder auf dem auf der Rechnung angegebenen Weg zahlbar. Bei Zahlungsverzug können wir die Arbeit oder den Dienst bis zum Zahlungseingang pausieren."]),
 ("5. Korrekturen und Abnahme", ["Jedes Angebot enthält bis zu zwei Korrekturschleifen im vereinbarten Umfang. Neue Funktionen oder Änderungen des Umfangs werden gesondert angeboten.",
   "Das Ergebnis gilt als abgenommen, wenn Sie es bestätigen oder produktiv nutzen oder 7 Tage nach Lieferung keine begründeten Mängel gemeldet wurden."]),
 ("6. Gewährleistung und Support", ["Fehler in unserer eigenen Arbeit, die innerhalb von 30 Tagen nach Lieferung gemeldet werden, beheben wir kostenlos. Ausgenommen sind Änderungen durch Dritte, Änderungen externer Dienste (z. B. neue Regeln oder APIs von Instagram, TikTok, Telegram oder KI-Anbietern) sowie neue Anforderungen.",
   "KI-Agenten arbeiten mit probabilistischen Modellen und können Fehler machen. Wir konfigurieren und testen sie sorgfältig mit Ihnen; die Prüfung wichtiger Antworten und der Einsatz im eigenen Unternehmen liegen in der Verantwortung des Kunden."]),
 ("7. Nutzungsrechte", ["Nach vollständiger Bezahlung erhalten Sie das zeitlich und räumlich unbeschränkte Recht, die gelieferten Ergebnisse (Texte, Designs, Videos, Code) für Ihr Unternehmen zu nutzen. Wir dürfen das Projekt in unserem Portfolio zeigen, sofern Sie nicht widersprechen. Komponenten Dritter (Open-Source-Bibliotheken, Schriften, Stock-Medien, KI-Modelle) unterliegen ihren eigenen Lizenzen."]),
 ("8. Pflichten des Kunden", ["Sie stellen sicher, dass bereitgestellte Materialien keine Rechte Dritter verletzen und dass der Einsatz des Agenten bzw. der Inhalte den für Ihr Unternehmen geltenden Gesetzen und Plattformregeln entspricht (Werbung, Datenschutz, Verbraucherrecht)."]),
 ("9. Haftung", ["Wir haften unbeschränkt bei Vorsatz und grober Fahrlässigkeit. Im Übrigen ist die Haftung auf die Vergütung für die betroffene Leistung begrenzt; die Haftung für entgangenen Gewinn und mittelbare Schäden ist ausgeschlossen, soweit gesetzlich zulässig. Zwingende Verbraucherrechte bleiben unberührt."]),
 ("10. Kündigung und Widerruf", ["Sie können ein einmaliges Projekt jederzeit beenden. Bis dahin erbrachte Leistungen werden vergütet; die Anzahlung wird verrechnet, ein Überschuss erstattet.",
   "Verbraucher in der EU haben bei Fernabsatzverträgen ein 14-tägiges Widerrufsrecht. Verlangen Sie den Beginn der Arbeiten innerhalb dieser Frist, zahlen Sie im Fall des Widerrufs den bereits erbrachten Teil; das Widerrufsrecht erlischt, sobald die Leistung vollständig erbracht ist."]),
 ("11. Schlussbestimmungen", ["Ist eine Bestimmung unwirksam, bleibt der Rest wirksam. Fragen zu diesen Bedingungen: " + CONTACT + "."]),
],
"ru": [
 ("1. Область действия", ["Эти условия действуют для всех услуг VA Corporation: AI-агенты, автоматизация, SMM и видео на ИИ, Telegram-боты, сайты, дашборды и игры. Индивидуальные договорённости в письменном виде (достаточно сообщения или e-mail) имеют приоритет."]),
 ("2. Цены", ["Все цены на сайте — стартовые, в евро, без НДС; НДС добавляется, если этого требует закон. Точная стоимость фиксируется в письменном предложении после короткой бесплатной консультации, в зависимости от объёма проекта.",
   "Ежемесячное обслуживание и поддержка не входят в разовую стоимость. Их цена зависит от сложности проекта и согласуется в предложении. Расходы третьих сторон (использование AI-моделей, хостинг, домены, платные API, сборы магазинов приложений и рекламы) клиент оплачивает напрямую либо они перевыставляются по себестоимости, если не договорились иначе."]),
 ("3. Как идёт проект", ["1) Бесплатная консультация — уточняем цель. 2) Письменное предложение: объём, цена, этапы и сроки. 3) Предоплата и старт. 4) Прототип или первая версия для ваших комментариев. 5) Правки, сдача и запуск. 6) По желанию — обслуживание.",
   "Сроки начинаются после получения предоплаты и всех материалов и доступов от вас (тексты, логотипы, аккаунты, данные). Задержки из-за отсутствия материалов или обратной связи соответственно сдвигают сроки."]),
 ("4. Оплата", ["Разовые проекты: 50 % предоплата до начала работ и 50 % при сдаче, до финальной передачи или запуска. Проекты дороже 3 000 € можно разбить на этапы (например, 40 % / 30 % / 30 %).",
   "Ежемесячные услуги (пакеты AI SMM, обслуживание, работа агентов): оплата помесячно вперёд. Минимальный срок — один месяц; отказаться можно в любой момент с окончанием оплаченного месяца.",
   "Счета оплачиваются в течение 7 дней банковским переводом или иным способом, указанным в счёте. При просрочке оплаты мы можем приостановить работы или услугу до поступления оплаты."]),
 ("5. Правки и приёмка", ["Каждое предложение включает до двух кругов правок в рамках согласованного объёма. Новые функции или изменение объёма оцениваются отдельно.",
   "Результат считается принятым, когда вы его подтвердили или начали использовать, либо через 7 дней после сдачи, если обоснованные недостатки не заявлены."]),
 ("6. Гарантия и поддержка", ["Ошибки в нашей работе, о которых сообщили в течение 30 дней после сдачи, исправляем бесплатно. Это не касается изменений, внесённых третьими лицами, изменений внешних сервисов (например, новых правил или API Instagram, TikTok, Telegram или AI-провайдеров) и новых требований.",
   "AI-агенты работают на вероятностных моделях и могут ошибаться. Мы тщательно настраиваем и тестируем их вместе с вами, но проверка важных ответов и то, как агент используется в бизнесе, — ответственность клиента."]),
 ("7. Права на результаты", ["После полной оплаты вы получаете право использовать результаты (тексты, дизайн, видео, код) в своём бизнесе без ограничений по сроку и территории. Мы можем показывать проект в портфолио, если вы не против. Компоненты третьих сторон (open-source библиотеки, шрифты, стоковые материалы, AI-модели) остаются под своими лицензиями."]),
 ("8. Обязанности клиента", ["Вы гарантируете, что переданные материалы не нарушают права третьих лиц, а использование агента или контента соответствует законам и правилам платформ, действующим для вашего бизнеса (реклама, защита данных, права потребителей)."]),
 ("9. Ответственность", ["Мы несём неограниченную ответственность за умысел и грубую небрежность. В остальных случаях ответственность ограничена суммой, оплаченной за соответствующую услугу; ответственность за упущенную выгоду и косвенный ущерб исключена в пределах, допустимых законом. Обязательные права потребителей не затрагиваются."]),
 ("10. Расторжение и отказ", ["Вы можете остановить разовый проект в любой момент. Выполненная к этому моменту работа оплачивается; предоплата засчитывается, остаток возвращается.",
   "Потребители в ЕС имеют право отказаться от дистанционного договора в течение 14 дней. Если вы просите начать работу в этот срок, при отказе оплачивается уже выполненная часть; право на отказ прекращается после полного оказания услуги."]),
 ("11. Заключительные положения", ["Если какое-либо положение недействительно, остальные сохраняют силу. Вопросы по условиям: " + CONTACT + "."]),
],
}

PRIVACY = {
"en": [
 ("1. Who is responsible", ["Controller of this website: VA Corporation. Contact: " + CONTACT + "."]),
 ("2. Visiting the website", ["The website is a static site hosted on GitHub Pages (GitHub, Inc., USA). When you open a page, GitHub processes technical data such as your IP address, date and time, browser and requested page to deliver the site and keep it secure (legitimate interest, Art. 6(1)(f) GDPR). See GitHub's privacy statement for details.",
   "Advertising (Meta Pixel): only if you click “Accept” in the cookie banner, the site loads the Meta Pixel (Meta Platforms Ireland Ltd.). It sets cookies and sends Meta which pages you visited and whether you clicked WhatsApp or Telegram, so that we can show you our ads on Facebook and Instagram and measure them (consent, Art. 6(1)(a) GDPR; § 25(1) TDDDG). Meta may process data in the USA. If you click “Decline”, nothing is loaded. You can change your choice at any time by deleting the site data (“va-consent”) in your browser. Your browser also stores your language choice (localStorage) and an offline copy of the pages (service worker cache) only on your device; you can delete them in your browser settings."]),
 ("3. Contact form and messengers", ["The contact form does not send data to our servers: it prepares your message and opens WhatsApp, Telegram or Instagram, where you send it yourself. These services are run by Meta Platforms and Telegram under their own privacy policies. We use your name, contact and request only to answer you and to prepare an offer (Art. 6(1)(b) GDPR) and delete them when they are no longer needed, unless the law requires us to keep them (for example invoices)."]),
 ("4. Videos, fonts and links", ["Videos on the site are loaded from our own repository on GitHub. Fonts are stored on our site, no external font services are used. Links to other websites (news sources, social networks) are only opened when you click them."]),
 ("5. Social media", ["When you interact with our pages on Instagram, Facebook or TikTok, the operators of these platforms process your data under their own policies. Our AI agent may answer comments and messages there on our behalf; the replies are marked as written by our SMM agent."]),
 ("6. Your rights", ["You have the right to access, rectification, erasure, restriction of processing, data portability and objection, and the right to lodge a complaint with a data protection authority. To use these rights, write to us via the contacts above."]),
 ("7. Changes", ["We update this policy when our services change. The current version is always on this page."]),
],
"de": [
 ("1. Verantwortlicher", ["Verantwortlich für diese Website: VA Corporation. Kontakt: " + CONTACT + "."]),
 ("2. Besuch der Website", ["Die Website ist eine statische Seite auf GitHub Pages (GitHub, Inc., USA). Beim Aufruf verarbeitet GitHub technische Daten wie IP-Adresse, Datum und Uhrzeit, Browser und aufgerufene Seite, um die Seite auszuliefern und abzusichern (berechtigtes Interesse, Art. 6 Abs. 1 lit. f DSGVO). Einzelheiten in der Datenschutzerklärung von GitHub.",
   "Werbung (Meta Pixel): Nur wenn Sie im Cookie-Banner auf „Akzeptieren“ klicken, lädt die Website das Meta Pixel (Meta Platforms Ireland Ltd.). Es setzt Cookies und übermittelt an Meta, welche Seiten Sie besucht haben und ob Sie auf WhatsApp oder Telegram geklickt haben, damit wir Ihnen unsere Anzeigen auf Facebook und Instagram zeigen und auswerten können (Einwilligung, Art. 6 Abs. 1 lit. a DSGVO; § 25 Abs. 1 TDDDG). Meta kann Daten in den USA verarbeiten. Klicken Sie auf „Ablehnen“, wird nichts geladen. Sie können Ihre Wahl jederzeit ändern, indem Sie die Website-Daten („va-consent“) in Ihrem Browser löschen. Ihr Browser speichert außerdem Ihre Sprachwahl (localStorage) und eine Offline-Kopie der Seiten (Service-Worker-Cache) nur auf Ihrem Gerät; Sie können beides in den Browsereinstellungen löschen."]),
 ("3. Kontaktformular und Messenger", ["Das Kontaktformular sendet keine Daten an unsere Server: Es bereitet Ihre Nachricht vor und öffnet WhatsApp, Telegram oder Instagram, wo Sie sie selbst absenden. Diese Dienste werden von Meta Platforms bzw. Telegram nach eigenen Datenschutzbestimmungen betrieben. Name, Kontakt und Anfrage nutzen wir nur zur Beantwortung und Angebotserstellung (Art. 6 Abs. 1 lit. b DSGVO) und löschen sie, sobald sie nicht mehr benötigt werden, soweit keine gesetzlichen Aufbewahrungspflichten bestehen (z. B. Rechnungen)."]),
 ("4. Videos, Schriften und Links", ["Videos werden aus unserem eigenen Repository auf GitHub geladen. Schriften liegen auf unserer Website, externe Schriftdienste werden nicht genutzt. Links zu anderen Websites (Nachrichtenquellen, soziale Netzwerke) werden erst beim Anklicken geöffnet."]),
 ("5. Soziale Netzwerke", ["Wenn Sie mit unseren Seiten auf Instagram, Facebook oder TikTok interagieren, verarbeiten die Betreiber Ihre Daten nach eigenen Richtlinien. Unser KI-Agent kann dort in unserem Namen auf Kommentare und Nachrichten antworten; diese Antworten sind als vom SMM-Agenten verfasst gekennzeichnet."]),
 ("6. Ihre Rechte", ["Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch sowie auf Beschwerde bei einer Datenschutzaufsichtsbehörde. Schreiben Sie uns dazu über die oben genannten Kontakte."]),
 ("7. Änderungen", ["Wir passen diese Erklärung an, wenn sich unsere Dienste ändern. Die aktuelle Fassung finden Sie immer auf dieser Seite."]),
],
"ru": [
 ("1. Ответственное лицо", ["Ответственный за этот сайт: VA Corporation. Контакты: " + CONTACT + "."]),
 ("2. Посещение сайта", ["Сайт статический и размещён на GitHub Pages (GitHub, Inc., США). При открытии страницы GitHub обрабатывает технические данные — IP-адрес, дату и время, браузер и запрошенную страницу — чтобы показать сайт и защитить его (законный интерес, ст. 6(1)(f) GDPR). Подробнее — в политике конфиденциальности GitHub.",
   "Реклама (пиксель Meta): только если вы нажмёте «Принять» в окне cookie, сайт загружает пиксель Meta (Meta Platforms Ireland Ltd.). Он ставит cookie и передаёт Meta, какие страницы вы посетили и нажимали ли вы WhatsApp или Telegram, чтобы мы могли показывать вам нашу рекламу в Facebook и Instagram и оценивать её (согласие, ст. 6(1)(a) GDPR; § 25(1) TDDDG). Meta может обрабатывать данные в США. Если нажать «Отклонить», ничего не загружается. Изменить выбор можно в любой момент, удалив данные сайта («va-consent») в браузере. Кроме того, браузер хранит выбранный язык (localStorage) и офлайн-копию страниц (кэш service worker) только на вашем устройстве; их можно удалить в настройках браузера."]),
 ("3. Форма заявки и мессенджеры", ["Форма заявки не отправляет данные на наши серверы: она готовит ваше сообщение и открывает WhatsApp, Telegram или Instagram, где вы сами его отправляете. Эти сервисы работают по собственным правилам Meta Platforms и Telegram. Имя, контакт и запрос мы используем только чтобы ответить и подготовить предложение (ст. 6(1)(b) GDPR) и удаляем, когда они больше не нужны, если закон не требует их хранить (например, счета)."]),
 ("4. Видео, шрифты и ссылки", ["Видео загружаются из нашего собственного репозитория на GitHub. Шрифты хранятся на нашем сайте, внешние сервисы шрифтов не используются. Ссылки на другие сайты (источники новостей, соцсети) открываются только при нажатии."]),
 ("5. Социальные сети", ["Когда вы взаимодействуете с нашими страницами в Instagram, Facebook или TikTok, ваши данные обрабатывают операторы этих платформ по своим правилам. Наш AI-агент может отвечать там на комментарии и сообщения от нашего имени; такие ответы помечены как созданные SMM-агентом."]),
 ("6. Ваши права", ["Вы вправе получить доступ к данным, исправить, удалить их, ограничить обработку, получить их в переносимом виде, возразить против обработки и подать жалобу в надзорный орган по защите данных. Для этого напишите нам по контактам выше."]),
 ("7. Изменения", ["Мы обновляем политику при изменении наших сервисов. Актуальная версия всегда на этой странице."]),
],
}

DOCS = {"terms": TERMS, "privacy": PRIVACY}
LANGS = ["en", "de", "ru"]


def path(doc, l):
    return f"{news.prefix(l)}{doc}/" if l in LANGS else f"{doc}/"


def links(l):
    """Footer links for any language (falls back to English)."""
    u = UI.get(l, UI["en"])
    return f'<a href="/{path("terms", l)}">{e(u[2])}</a><a href="/{path("privacy", l)}">{e(u[3])}</a>'


def build_all():
    entries = []
    for doc, data in DOCS.items():
        alts = [(l, BASE + path(doc, l)) for l in LANGS]
        for l in LANGS:
            u = UI[l]
            body = "".join(f"<h2>{e(h)}</h2>" + "".join(f"<p>{e(p)}</p>" for p in ps) for h, ps in data[l])
            other = '<nav class="langs" aria-label="Language">' + "".join(
                f'<a href="/{path(doc, o)}" hreflang="{o}"{" aria-current=\"true\"" if o == l else ""}>{news.LANG_NAME[o]}</a>' for o in LANGS) + "</nav>"
            html = (f'<article><p class="kicker">VA Corporation · {e(u[1])}</p><h1>{e(TITLES[doc][l])}</h1>'
                    f'<p class="lead">{e(u[0])}: {UPDATED}</p>{body}{other}</article>')
            canon = BASE + path(doc, l)
            ld = {"@context": "https://schema.org", "@type": "WebPage", "name": TITLES[doc][l], "url": canon, "inLanguage": l, "dateModified": UPDATED}
            h = news.page(l, f"{TITLES[doc][l]} — VA Corporation", TITLES[doc][l], canon, alts, html, ld)
            h = h.replace(f'<a href="{news.index_url(l)}" aria-current="page">', f'<a href="{news.index_url(l)}">', 1)
            out = path(doc, l) + "index.html"
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, "w", encoding="utf-8").write(h)
            entries.append((canon, UPDATED, alts))
    return entries
