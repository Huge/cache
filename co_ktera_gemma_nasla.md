A. Nálezy v curlie (kde modely excelovaly)
Kvadratická alokace paměti 𝑂(𝑁^2) a OOM DoS v formatter/json.go:
Podstata: Proměnná j.level inkrementuje při každé otevírací závorce { nebo [. Při odsazování se volá bytes.Repeat(indent, j.level). Pro 𝑁 zanořených závorek alokace roste kvadraticky(≈2𝑁^2 bajtů), což bleskově shodí proces na OOM panic.
Kdo to našel a potvrdil: ThinkingCap-26B (Q4_K_M) a referenční Vertex MaaS.
Nekonečný růst bufferu bez nového řádku v formatter/color.go:
Podstata: HeaderColorizer.Write akumuluje příchozí bajty do c.line a flush/reset provede teprve při znaku \n. Pokud útočník pošle dlouhý datový proud bez odřádkování, buffer roste bez horního limitu až do vyčerpání RAM.
Kdo to našel a potvrdil: ThinkingCap-26B (Q4_K_M), 12B (UD-Q4_K_XL), 12B (UD-Q6_K_XL) a Vertex MaaS.
Nekonečné načítání vstupu z -d flagu a piped stdin v main.go:
Podstata: Curlie načítá tělo požadavku do dynamického bytes.Buffer bez použití io.LimitReader.
Kdo to našel: 12B (UD-Q4_K_XL), 12B (IQ4_XS) a Bonsai-27B (PTQ1_0).
Trvalé potlačení výstupu (Sticky suppression) v formatter/binaryfilter.go:
Podstata: Jakmile filtr narazí na nulový bajt 0x00, nastaví vnitřní flag ignore = true. Protože instance filtru žije dál, potlačí se veškerý následný výstup programu včetně chybových hlášek.
Kdo to našel: 12B (UD-Q4_K_XL).
B. Nálezy v yopass (komplexní doménová logika)
Proxy Spoofing / Cookie Authentication DoS v pkg/server/oidc.go:
Podstata: Funkce isSecure slepě věří hlavičce X-Forwarded-Proto: https, pokud není nastaven whitelist proxy. Útočník přes obyčejné HTTP pošle tuto hlavičku, server nastaví na session cookie příznak Secure, ale browser ji přes nešifrované HTTP odmítne uložit. Uživatel se nemůže přihlásit (DoS autentizace).
Kdo to našel: ThinkingCap-26B (Q6_K) a 12B (UD-Q6_K_XL).
Fail-open Session Revocation při výpadku DB v pkg/server/oidc.go:
Podstata: Funkce sessionRevoked při chybě spojení s databází vrátí false (místo pádu či odepření přístupu). Server považuje session za platnou, což umožňuje obejít revokaci vyvoláním DoS na databázi.
Kdo to našel: 12B (UD-Q4_K_XL).
Ground truth (chybějící validace email_verified):
Všechny modely tento nález buď v triáži zamítly jako nízkou závažnost (spoléhaly na upstream IdP), nebo jej nezachytily kvůli chybějícímu kontextu celé OIDC specifikace.
