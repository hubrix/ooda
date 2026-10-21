// ooda — desktop half. Pane + palette commands + status chip.
// Loaded uncompiled: jsx() calls only, imports limited to the SDK and react.

import { host, haptic, useQuery, useValue, PALETTE_AREA } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

const STAGES = ['observe', 'orient', 'decide', 'act']

const STAGE_LABEL = {
  observe: 'Observe',
  orient: 'Orient',
  decide: 'Decide',
  act: 'Act'
}

function StageRail({ stage }) {
  return jsx('div', {
    className: 'flex items-center gap-1',
    children: STAGES.map((s) =>
      jsx('div', {
        key: s,
        title: STAGE_LABEL[s],
        className:
          'h-1 flex-1 rounded-full ' +
          (STAGES.indexOf(s) <= STAGES.indexOf(stage)
            ? 'bg-(--ui-accent)'
            : 'bg-(--ui-stroke-secondary)')
      })
    )
  })
}

function PromptRow({ p, onRun }) {
  return jsxs('button', {
    type: 'button',
    onClick: () => onRun(p),
    className:
      'w-full text-left rounded-md px-2 py-1.5 hover:bg-(--ui-accent)/10 flex flex-col gap-0.5',
    children: [
      jsxs('div', {
        className: 'flex items-center gap-2',
        children: [
          jsx('span', {
            className: 'text-[0.625rem] uppercase tracking-wide text-(--ui-text-quaternary)',
            children: p.stage
          }),
          jsx('span', { className: 'text-xs font-medium truncate', children: p.title })
        ]
      }),
      jsx('div', {
        className: 'text-[0.6875rem] text-(--ui-text-quaternary) line-clamp-2',
        children: p.why
      })
    ]
  })
}

function OodaPane({ ctx }) {
  const active = useQuery({
    queryKey: ['ooda', 'active'],
    queryFn: () => ctx.rest('/active'),
    refetchInterval: 5000
  })
  const promptList = useQuery({
    queryKey: ['ooda', 'prompts'],
    queryFn: () => ctx.rest('/prompts')
  })

  const loop = active.data?.loop ?? null
  const prompts = promptList.data?.prompts ?? []

  const run = async (p) => {
    haptic('tap')
    const situation = loop?.situation ?? ''
    const text = situation
      ? p.prompt.replace(/\[[^\]]*\]/, `[${situation}]`)
      : p.prompt
    const sid = host.state.focusedSessionId.get()
    const inserted = await host.composer.insertText(sid, text, { mode: 'block' })
    if (inserted) host.composer.focus(sid)
  }

  const startLoop = async () => {
    const draft = (await host.composer.getDraft(host.state.focusedSessionId.get())) ?? ''
    const situation = draft.trim() || 'the situation in this chat'
    await ctx.rest('/loops', { method: 'POST', body: { situation } })
    active.refetch()
    host.notify({ kind: 'info', message: `OODA loop opened: ${situation.slice(0, 60)}` })
  }

  return jsxs('div', {
    className: 'flex h-full flex-col gap-2 p-3 text-sm overflow-hidden',
    children: [
      jsxs('div', {
        className: 'flex items-center justify-between',
        children: [
          jsx('div', { className: 'font-medium', children: 'OODA' }),
          jsx('button', {
            type: 'button',
            onClick: startLoop,
            className:
              'text-[0.6875rem] px-2 py-0.5 rounded border border-(--ui-stroke-secondary) hover:bg-(--ui-accent)/10',
            children: 'New loop'
          })
        ]
      }),

      loop
        ? jsxs('div', {
            className: 'flex flex-col gap-1.5 rounded-md border border-(--ui-stroke-secondary) p-2',
            children: [
              jsx(StageRail, { stage: loop.stage }),
              jsx('div', {
                className: 'text-xs text-(--ui-text-secondary) line-clamp-3',
                children: loop.situation
              }),
              jsxs('div', {
                className: 'text-[0.6875rem] text-(--ui-text-quaternary)',
                children: [`stage ${loop.stage}`, ' · ', `${loop.entries.length} entries`]
              })
            ]
          })
        : jsx('div', {
            className: 'text-xs text-(--ui-text-quaternary)',
            children: 'No open loop. Type a situation in the composer, then New loop.'
          }),

      jsx('div', {
        className: 'text-[0.6875rem] uppercase tracking-wide text-(--ui-text-quaternary) pt-1',
        children: 'Boyd prompts — click to insert'
      }),

      jsx('div', {
        className: 'flex-1 overflow-y-auto flex flex-col gap-0.5',
        children: prompts.map((p) => jsx(PromptRow, { key: p.key, p, onRun: run }))
      })
    ]
  })
}

export default {
  id: 'ooda',
  name: 'OODA',
  defaultEnabled: false,
  register(ctx) {
    ctx.register({
      id: 'pane',
      area: 'panes',
      title: 'ooda',
      data: { placement: 'right', width: '300px' },
      render: () => jsx(OodaPane, { ctx })
    })

    ctx.register({
      id: 'chip',
      area: 'statusBar.right',
      order: 140,
      render: () => {
        const active = useQuery({
          queryKey: ['ooda', 'active'],
          queryFn: () => ctx.rest('/active'),
          refetchInterval: 5000
        })
        const loop = active.data?.loop
        return jsx('button', {
          type: 'button',
          className: 'px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
          onClick: () => {
            haptic('tap')
            host.notify({
              kind: 'info',
              message: loop ? `OODA ${loop.id} · ${loop.stage}` : 'No open OODA loop'
            })
          },
          children: loop ? `ooda:${loop.stage}` : 'ooda'
        })
      }
    })

    ctx.register({
      id: 'cmd-full',
      area: PALETTE_AREA,
      data: {
        label: 'OODA: run the full Boyd loop',
        run: async () => {
          const sid = host.state.focusedSessionId.get()
          const draft = (await host.composer.getDraft(sid)) ?? ''
          const text = draft.trim() || 'the situation in this chat'
          await ctx.rest('/loops', { method: 'POST', body: { situation: text } })
          const p = (await ctx.rest('/prompts')).prompts.find((x) => x.key === 'full-boyd-loop')
          await host.composer.insertText(sid, p.prompt, { mode: 'block' })
          host.composer.focus(sid)
        }
      }
    })

    ctx.register({
      id: 'cmd-status',
      area: PALETTE_AREA,
      data: {
        label: 'OODA: show active loop',
        run: async () => {
          const { loop } = await ctx.rest('/active')
          if (!loop) return host.notify({ kind: 'info', message: 'No open OODA loop' })
          const lines = [
            `Loop ${loop.id} — ${loop.stage} (${loop.status})`,
            loop.situation,
            ...loop.entries.map((e) => `- (${e.stage}) ${e.content}`)
          ]
          await host.composer.insertText(null, lines.join('\n'), { mode: 'block' })
        }
      }
    })
  }
}
