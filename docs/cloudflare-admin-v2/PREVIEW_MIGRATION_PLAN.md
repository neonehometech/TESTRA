# TESTRA — Cloudflare Admin V2 Preview Migration

Status: OWNER DIRECTION CONFIRMED / IMPLEMENTATION PENDING
Branch: feat/cloudflare-admin-v2-preview
Production: DO NOT MODIFY

## Objective
Replace Supabase with Cloudflare Workers, D1 and R2, while preserving existing TESTRA public website and admin interface pixel-for-pixel where practical. Maintain original /admin.html entry route. Create a new secure administrator login. No real customer orders have been placed; testing records need not be migrated, but verify and preserve useful product, pricing, content and media configuration before decommissioning Supabase.

## Verified repository inventory (initial audit)
- admin.html — existing admin entry shell.
- admin-core.html — mobile/core admin, Supabase password login and orders, shipments, events, reviews.
- admin-desktop.html — desktop admin, Supabase password login and same data surfaces.
- checkout.html — packages, products, orders and order_items.
- pricing-settings.html — packages and Supabase OTP authentication.
- review.html — products, reviews and review-images storage.
- index.html — review integration and storefront.
- admin-delete-order.js — Supabase-dependent delete flow.
- inventory-mockup.html — prototype, not evidence of a complete inventory backend.
- supabase/migrations/001_ecommerce_foundation.sql — defines testra_* tables, which differ from unprefixed tables used in current frontend. DO NOT treat this SQL as authoritative live schema.

## Preview-only implementation sequence
1. Capture admin UI baseline screenshots at mobile/tablet/desktop sizes; inventory all buttons, workflows, states and actual vs mock features.
2. Inventory current Supabase live schema, tables, RPC, buckets and row counts if authorized access exists. If inaccessible, document missing configuration and recreate necessary TESTRA catalog settings from approved sources; never assume live values.
3. Create isolated Cloudflare Preview Worker, D1 database, R2 bucket, secrets and Preview URL; no production bindings.
4. Implement versioned SQLite migrations for catalog, packages/prices, orders/items, payment/shipment events, reviews, media metadata, inventory, admin users/sessions and audit events. Store currency as integer cents, preserve referential integrity and avoid client-controlled totals.
5. Implement server-side admin bootstrap using one-time secret, securely hashed passwords, HttpOnly Secure SameSite cookies, CSRF protections, rate limiting, session revocation and role authorization. Never commit secrets or use Supabase password hashes.
6. Implement Worker API endpoints with input validation and authorization. Public checkout creates orders server-side and never exposes private customer data. Payment confirmation requires verified provider evidence, not a public client flag.
7. Migrate necessary media to R2 with MIME/type/size controls and appropriate private/public access; preserve originals and map URLs.
8. Adapt existing frontend data calls while keeping DOM, CSS, responsive layouts and routes unchanged. Retain TESTRA branding; do not refactor into NEONE.CORE yet.
9. Validate admin sign-in/sign-out, first-admin setup, orders, product pricing, checkout, inventory, reviews, media, authorization and responsive UI in Preview. Ensure no live production payment/webhook side effects.
10. Reconcile catalog/media settings and test end-to-end; prepare documented cutover and rollback. Require separate owner approval before any merge, production deployment, DNS change or Supabase deletion.

## Open blockers and explicit non-assumptions
- Live Supabase schema and data counts are not yet verified.
- Actual Cloudflare Preview D1/R2 resources, account access and secrets are not yet provisioned.
- Inventory and some admin sections may be mockups; do not claim functionality until tested.
- No deployment, migration execution or successful admin login has occurred.

## Acceptance criteria
- Admin UI visually matches original across supported breakpoints.
- New login works independently of Supabase.
- Every existing functioning workflow has tested parity; mockup gaps are reported.
- D1/R2/Worker Preview fully isolated from Production.
- All required catalog, prices and media preserved or owner-approved for recreation.
- Production remains unchanged until explicit owner approval.
