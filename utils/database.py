import aiosqlite

DB = "bot.db"

async def setup_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS economy (
            guild_id INTEGER,
            user_id INTEGER,
            coins INTEGER,
            PRIMARY KEY (guild_id, user_id)
        )""")

        await db.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            guild_id INTEGER,
            channel_id INTEGER
        )""")

        await db.execute("""
        CREATE TABLE IF NOT EXISTS premium (
            guild_id INTEGER PRIMARY KEY,
            active INTEGER
        )""")

        await db.commit()

# ECONOMY
async def get_balance(g, u):
    async with aiosqlite.connect(DB) as db:
        c = await db.execute("SELECT coins FROM economy WHERE guild_id=? AND user_id=?", (g,u))
        r = await c.fetchone()
        return r[0] if r else 0

async def add_coins(g, u, amt):
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        INSERT INTO economy VALUES (?,?,?)
        ON CONFLICT(guild_id,user_id) DO UPDATE SET coins=coins+?
        """,(g,u,amt,amt))
        await db.commit()

# CHANNELS
async def get_channels(g):
    async with aiosqlite.connect(DB) as db:
        c = await db.execute("SELECT channel_id FROM channels WHERE guild_id=?", (g,))
        return [i[0] for i in await c.fetchall()]

async def add_channel(g,cid):
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT INTO channels VALUES (?,?)",(g,cid))
        await db.commit()

# PREMIUM
async def is_premium(g):
    async with aiosqlite.connect(DB) as db:
        c = await db.execute("SELECT active FROM premium WHERE guild_id=?", (g,))
        r = await c.fetchone()
        return r and r[0]==1
