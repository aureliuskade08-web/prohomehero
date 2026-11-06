"""Content for the service pages. One entry per page; build_pages.py turns each into services/<slug>/index.html.

To add a page: copy an entry, change the slug, text and photo, add it to ORDER, then run
    python3 build_pages.py
The sitemap, structured data, internal links and the form topic are all generated from the entry.
Write only what is true for the business. Do not add prices, timelines, warranties, reviews or places we do not serve.
"""

# photo numbers refer to images/kitchen-NN.jpg (captions live in build.py)
PAGES = {
    "kitchen-remodeling": {
        "name": "Full kitchen remodels",
        "service_value": "Full kitchen remodel",
        "title": "Kitchen Remodeling | Licensed and Insured | Home Hero",
        "description": "Full kitchen remodels from layout and demolition to finish work, by one licensed and insured team. Financing available. Get a free estimate.",
        "h1": "Kitchen remodeling, planned and built by one team",
        "lead": "One team designs and builds your kitchen, so the plan you approve is the kitchen you get.",
        "photo": 19,
        "photo_alt": "White shaker kitchen with a stainless gas range, quartz counters and a tile floor",
        "included_title": "What a full remodel covers",
        "included": [
            ("Layout and design", "We measure the room, talk through how you cook and entertain, and settle the layout before anything is ordered."),
            ("Demolition and preparation", "The old kitchen comes out and the room is made ready for the new cabinets, counters and finishes."),
            ("Cabinets, counters and backsplash", "Shaker or flat-panel cabinetry, quartz or granite counters, and tile or slab backsplash chosen to work together."),
            ("Sinks, lighting and flooring", "Sinks and faucets, pendant and under-cabinet lighting, and plank or tile flooring finish the room."),
        ],
        "options_title": "Questions to settle early",
        "options": [
            ("Keep the layout or change it", "Keeping the sink and range where they are is simpler. Moving them or opening a wall to the next room changes the plan, and we talk through which is worth it for your kitchen."),
            ("Where to spend and where to save", "Cabinets and counters are usually the biggest line items. We help you decide where a higher-end finish matters to you and where a simpler one does the job."),
            ("Choosing finishes together", "Colors and materials look different in a real kitchen than on a sample. Our finishes designer on the home page lets you try combinations before you commit."),
        ],
        "faq": [
            ("How do I get started?", "Ask for a free estimate. We visit, listen to how you use the kitchen and measure the space, then you choose finishes and receive a written estimate before any work begins."),
            ("Can I pay over time?", "Ask about financing when we quote your project. Financing is subject to approval."),
        ],
        "related": ["cabinets", "countertops-backsplash", "kitchen-islands"],
    },
    "cabinets": {
        "name": "Cabinets and storage",
        "service_value": "Cabinets",
        "title": "Kitchen Cabinets and Storage | Home Hero",
        "description": "Shaker kitchen cabinets, pantry towers and glass-front uppers, installed by a licensed and insured remodeler. Free estimate and financing available.",
        "h1": "Kitchen cabinets that fit how you live",
        "lead": "Cabinets set the look of the room and do the daily work. We help you choose, then install.",
        "photo": 20,
        "photo_alt": "Navy cabinets with a quartz slab backsplash and a hardwood floor",
        "included_title": "Cabinet styles and storage",
        "included": [
            ("Shaker cabinets", "The classic five-piece door with a simple frame. It suits traditional and modern kitchens alike and shows up throughout our recent work."),
            ("Pantry towers", "Full-height cabinets give you storage for dry goods and small appliances without taking up counter space."),
            ("Glass-front uppers", "Glass doors let you show off dishes and break up a long wall of closed cabinets."),
            ("Two-tone kitchens", "Lighter uppers with darker base cabinets, such as white over navy or sage, add depth without making the room feel heavy."),
        ],
        "options_title": "Choices that change the look",
        "options": [
            ("Color", "White and cream keep a kitchen bright. Sage, green and navy add character. Our finishes designer lets you preview colors in a kitchen before you decide."),
            ("Hardware", "Brass, matte black and polished nickel pulls change the feel of the same cabinet. Long bar pulls read modern, smaller knobs read traditional."),
            ("Storage", "Think about what you reach for every day. Deep drawers for pots, a pantry tower, or a stacked glass upper can matter more than the door style."),
        ],
        "faq": [
            ("Do you install cabinets only, or the whole kitchen?", "Cabinets are one of our services and are part of every full remodel. Tell us what you have in mind in the estimate form and we will tell you what is involved."),
            ("How do I pick a color?", "Look at the light in your kitchen and the colors of your counters and floor. We can talk it through at the free estimate."),
        ],
        "related": ["kitchen-remodeling", "countertops-backsplash", "kitchen-islands"],
    },
    "countertops-backsplash": {
        "name": "Countertops and backsplash",
        "service_value": "Countertops and backsplash",
        "title": "Kitchen Countertops and Backsplash | Home Hero",
        "description": "Quartz and granite kitchen countertops with tile or slab backsplash, installed by a licensed and insured remodeler. Free estimate and financing.",
        "h1": "Countertops and backsplash that work together",
        "lead": "Counters take the most wear and the backsplash frames the room. We help you pick both.",
        "photo": 2,
        "photo_alt": "Quartz slab backsplash with a brass pull-down faucet and navy uppers with under-cabinet light",
        "included_title": "Materials we install",
        "included": [
            ("Quartz", "An engineered stone with consistent color and pattern. It does not need sealing and resists staining, which is why it is a common choice for busy kitchens."),
            ("Granite", "A natural stone, so every slab is different. It is durable and heat tolerant, and many types are sealed from time to time."),
            ("Slab backsplash", "Running the counter material up the wall gives a clean look with fewer grout lines to scrub."),
            ("Tile backsplash", "From classic subway tile to patterned shapes, tile adds texture and color and is easy to update later."),
        ],
        "options_title": "Things to weigh",
        "options": [
            ("Light or dark", "White and light counters make a room feel larger. Charcoal and soapstone-look counters feel dramatic and hide crumbs. Try both in our finishes designer."),
            ("Edges and overhangs", "A waterfall edge carries the stone down the side of an island. Standard edges are simpler. We can show you both."),
            ("Backsplash height", "A short splash is the budget choice. Running tile or slab to the upper cabinets or the ceiling makes the wall a feature."),
        ],
        "faq": [
            ("Which is better, quartz or granite?", "Neither wins for everyone. Quartz is low-maintenance and uniform. Granite is natural and unique. We walk through samples with you."),
            ("Can you match the backsplash to my counters?", "Yes. We help you choose a backsplash that complements the counter and cabinet colors."),
        ],
        "related": ["cabinets", "kitchen-islands", "sinks-fixtures"],
    },
    "kitchen-islands": {
        "name": "Islands and seating",
        "service_value": "Islands and seating",
        "title": "Kitchen Islands and Seating | Home Hero",
        "description": "Custom kitchen islands with seating and storage, sized to your room by a licensed and insured remodeler. Free estimate and financing available.",
        "h1": "A kitchen island sized to your room",
        "lead": "An island adds space, storage and seating when it fits. We size it to your room.",
        "photo": 18,
        "photo_alt": "Sage island with a brass faucet and pendant lights beside tall white pantry cabinets",
        "included_title": "What an island can do",
        "included": [
            ("Seating", "Stools along one side turn the island into a place for breakfast, homework and company while you cook."),
            ("Storage", "Drawers and cabinets on the working side keep pots, baking sheets and small appliances close."),
            ("Statement finishes", "Paint the island a different color from the perimeter cabinets, or run the counter down the sides in a waterfall edge."),
            ("Peninsula option", "When the room is too narrow for an island, a peninsula still adds seating and counter space."),
        ],
        "options_title": "Sizing it right",
        "options": [
            ("Room to move", "A common guideline is to leave about three to four feet of walkway around an island. We measure your kitchen to see what fits."),
            ("Seating overhang", "Stools need legroom, usually about a foot of overhang. We plan that into the counter so it is comfortable and supported."),
            ("Lighting above", "Pendant lights over the island make it a focal point. See the lighting and flooring page for ideas."),
        ],
        "faq": [
            ("Will an island fit in my kitchen?", "We measure at the free estimate and tell you honestly if an island, a smaller one or a peninsula suits the room better."),
            ("Can I preview island colors?", "Yes. In the finishes designer, choose an island color separate from your cabinets."),
        ],
        "related": ["kitchen-remodeling", "countertops-backsplash", "lighting-flooring"],
    },
    "sinks-fixtures": {
        "name": "Sinks, faucets and fixtures",
        "service_value": "Sinks and fixtures",
        "title": "Kitchen Sinks, Faucets and Fixtures | Home Hero",
        "description": "Farmhouse and workstation sinks, pull-down faucets, pot fillers and hardware, installed by a licensed and insured remodeler. Free estimate.",
        "h1": "Sinks and fixtures you will use every day",
        "lead": "The sink is where most kitchen work happens. We help you choose a sink, faucet and hardware.",
        "photo": 8,
        "photo_alt": "Brass pot filler over a gas cooktop with a quartz slab backsplash",
        "included_title": "Options we install",
        "included": [
            ("Farmhouse sinks", "A deep apron-front sink is a classic look and handles large pots and pans."),
            ("Workstation sinks", "Built-in ledges hold cutting boards and colanders so the sink doubles as prep space."),
            ("Pull-down faucets", "A spout that pulls down makes rinsing the sink and filling pots easier. Brass and matte black finishes are both popular in recent kitchens."),
            ("Pot fillers", "A faucet mounted over the range lets you fill a pot where you cook, so you carry less water."),
        ],
        "options_title": "Finishing touches",
        "options": [
            ("Match the metals", "Choose brass, matte black or polished nickel for the faucet, then repeat it in cabinet pulls and lighting. Try combinations in the finishes designer."),
            ("Mounting style", "An undermount sink sits below the counter for a smooth edge. A farmhouse sink shows its front panel. The counter material and cabinet base decide which works."),
            ("Think about use", "If you cook a lot, a larger single bowl or a workstation sink may beat a double bowl. We help you choose."),
        ],
        "faq": [
            ("Can you replace only the sink and faucet?", "Fixtures are one of our services. Describe what you have in mind in the estimate form and we will tell you what is involved."),
            ("Do the fixtures have to match?", "Not exactly, but a consistent metal finish looks pulled together."),
        ],
        "related": ["cabinets", "countertops-backsplash", "lighting-flooring"],
    },
    "lighting-flooring": {
        "name": "Lighting and flooring",
        "service_value": "Lighting and flooring",
        "title": "Kitchen Lighting and Flooring | Home Hero",
        "description": "Pendant and under-cabinet lighting plus plank and tile flooring, installed by a licensed and insured kitchen remodeler. Free estimate and financing.",
        "h1": "Kitchen lighting and flooring that finish the room",
        "lead": "Lighting sets the mood and flooring ties the colors together. We plan both with the kitchen.",
        "photo": 24,
        "photo_alt": "Green base cabinets with brass pulls and a black and white checkerboard floor",
        "included_title": "Lighting and floors we install",
        "included": [
            ("Pendant lights", "Hang pendants over an island or peninsula to light the work surface and give the room a focal point."),
            ("Under-cabinet lighting", "Light under the upper cabinets brightens the counters where you chop and cook, and glows softly in the evening."),
            ("Plank flooring", "Wood-look planks run through the kitchen into the next room and warm up a white or sage kitchen."),
            ("Tile flooring", "Large-format tile gives a clean, easy-to-wipe floor, while patterns such as a checkerboard add personality."),
        ],
        "options_title": "Planning tips",
        "options": [
            ("Layer the light", "Combine ceiling lights, pendants and under-cabinet lights so the kitchen works for cooking and for relaxing."),
            ("Think about the floor first", "A bold floor suits simpler cabinets. A quiet floor lets a strong cabinet color lead."),
            ("Match the finishes", "Repeat the hardware finish in your lighting so the room feels pulled together."),
        ],
        "faq": [
            ("Can I add lighting without a full remodel?", "Lighting is one of our services. Tell us what you want in the estimate form and we will explain the options."),
            ("What floor goes best with colorful cabinets?", "A neutral plank or light tile usually lets colored cabinets stand out. We can show you photos from our work."),
        ],
        "related": ["kitchen-islands", "sinks-fixtures", "kitchen-remodeling"],
    },
}

ORDER = ["kitchen-remodeling", "cabinets", "countertops-backsplash", "kitchen-islands", "sinks-fixtures", "lighting-flooring"]
