"""The Tapaia citizen cast for the character sheet (names from the prototype's seed users).
Outfits fit everyday Veridia: plain and band shirts [ch1], privacy robes hood down / hood up with the face cover
and its strap [ch1:132, ch1:140], neck bands [ch1]; tunics, cardigans, aprons, coats and scarves are our design
choices for a cosy town square."""

CAST = [
    ('Wren Halloway', 'herb grower, tea-cart regular', dict(
        skin='warm', hair='chestnut', hairstyle='short', eyes='green', expr='smile',
        outfit='tunic', top='leaf', bottom='brown', satchel=True, satchel_side=1)),
    ('Nessa Quill', 'runs the tea cart', dict(
        skin='fair', hair='ginger', hairstyle='bun', eyes='blue', expr='grin', freckles=True,
        outfit='apron', top='skyblue', over='parchment', bottom='charcoal', rolled=True, held='tea', pose='hold', hold_side=1)),
    ('Orla Fenwick', 'reads in the library', dict(
        skin='tan', hair='black', hairstyle='long', part=.18, eyes='brown', expr='calm', glasses=True,
        outfit='cardigan', top='plum', accent='cream', bottom='moss', bottom_kind='skirt', held='book', pose='hold', hold_side=1, book_col='maple')),
    ('Corvin Ashdale', 'robe, hood down, neck band', dict(
        skin='porcelain', hair='silver', hairstyle='swept', part=-.3, eyes='grey', expr='content', beard=True,
        outfit='robe', neckband=True)),
    ('Alder Meadows', 'robe, hood up, face cover', dict(
        skin='warm', hair='black', outfit='hood', eyes='brown', expr='smile')),
    ('Tobin Larkspur', 'band shirt, laughs easily', dict(
        skin='deep', hair='black', hairstyle='curly', eyes='brown', expr='laugh',
        outfit='bandtee', top='charcoal', accent='hydra', bottom='denim')),
    ('Odessa Brightmoss', 'elder, scarf and long coat', dict(
        skin='brown', hair='silver', hairstyle='elderbun', eyes='amber', expr='content',
        outfit='coat', top='wallblue', scarf='maple', bottom='charcoal', held='tea', pose='hold', hold_side=-1)),
    ('Pim Tallow', 'new in town, yellow shirt', dict(
        skin='porcelain', hair='blonde', hairstyle='ponytail', eyes='blue', expr='surprised',
        outfit='tee', top='hydra', bottom='denim', tail_side=1)),
    ('Juniper Vale', 'braid, cardigan, satchel', dict(
        skin='olive', hair='plum', hairstyle='braid', braid_side=-1, part=-.25, eyes='hazel', expr='wink',
        outfit='cardigan', top='sage', accent='white', bottom='brown', satchel=True, satchel_side=1)),
    ('Bram Teasel', 'tea house baker', dict(
        skin='fair', hair='auburn', hairstyle='crop', eyes='green', expr='smile', beard=True,
        outfit='apron', top='cream', over='moss', bottom='brown', rolled=True)),
    ('Lumi Ardent', 'robe, hood down, wavy hair', dict(
        skin='brown', hair='black', hairstyle='wavy', eyes='brown', expr='shy',
        outfit='robe', neckband=False)),
    ('Sorrel Finch', 'cosy cardigan, bob', dict(
        skin='warm', hair='auburn', hairstyle='bob', part=.3, eyes='hazel', expr='thoughtful',
        outfit='tee', top='teal', bottom='charcoal', scarf='mustard')),
]

# 3/4 views for two of them
TURNED = ['Nessa Quill', 'Alder Meadows']
