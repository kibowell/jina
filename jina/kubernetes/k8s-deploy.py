from jina import Flow

dump_path = '/shared'

# index_flow = (
#     Flow(name='index-flow')
#     .add(
#         name='cliptext',
#         uses='jinahub+docker://CLIPTextEncoder',
#         shards=1,
#         polling='any',
#     )
#     .add(
#         name='cliptext2',
#         uses='jinahub+docker://CLIPTextEncoder',
#         needs='gateway',
#         shards=1,
#         polling='any',
#     )
#     .add(
#         name='textindexer',
#         uses='jinahub+docker://PostgreSQLStorage',
#         needs=['cliptext'],
#     )
#     .add(
#         name='textindexer2',
#         uses='jinahub+docker://PostgreSQLStorage',
#         needs=['cliptext2'],
#     )
# )

search_flow = (
    Flow(name='search-flow', host='gateway.search-flow.svc.cluster.local')
    .add(
        name='cliptext',
        uses='jinahub+docker://CLIPTextEncoder',
        shards=2,
        peas_hosts=[
            f'{"cliptext-head"}.{"search-flow"}.svc.cluster.local',
            f'{"cliptext-tail"}.{"search-flow"}.svc.cluster.local',
            f'{"cliptext-pea-0"}.{"search-flow"}.svc.cluster.local',
            f'{"cliptext-pea-1"}.{"search-flow"}.svc.cluster.local',
        ],
        polling='all',
    ).build(copy_flow=True)
    # .add(
    #     name='cliptext2',
    #     uses='jinahub+docker://CLIPTextEncoder',
    #     needs='gateway',
    #     shards=1,
    #     polling='any',
    # )
    # .add(
    #     name='searcher1',
    #     shards=2,
    #     polling='all',
    #     uses='jinahub+docker://AnnoySearcher',
    #     uses_with={'dump_path': dump_path},
    #     uses_after='gcr.io/jina-showcase/match-merger',
    #     needs=['cliptext'],
    # )
    # .add(
    #     name='searcher2',
    #     shards=2,
    #     polling='all',
    #     uses='jinahub+docker://AnnoySearcher',
    #     uses_with={'dump_path': dump_path},
    #     uses_after='gcr.io/jina-showcase/match-merger',
    #     needs=['cliptext2'],
    # )
    # .add(
    #     name='ranker',
    #     uses='jinahub+docker://MinRanker',
    #     uses_with={'metric': 'cosine'},
    #     needs=['searcher1', 'searcher2'],
    # )
)

# print('deploy index flow')
# index_flow.plot('jina/kubernetes/index_flow.jpg')
# index_flow.deploy_naive('k8s')

print('deploy search flow')
# search_flow.plot('jina/kubernetes/search_flow.jpg')
search_flow.deploy_naive('k8s')
print('done')
